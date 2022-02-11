import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    '''
        This Lambda function, accepts an input from a workflow as JSON.
        {'division':'<value>'}
        Function parses the JSON input
        Function pulls the SSO permissionSet and inline policy
        Funcrtion checks if the division value exists in the inline policy
        If it exists: Do nothing and return back the response
        If it does not exists: Update the inline policy and return back the success/fail message
    '''
    logger.info('Event Variables triggered from an Okta Workflow')
    logger.info(event)
    division_value = event['division']
    logger.info('Value of division from the flow')
    logger.info(division_value)
    client = boto3.client('sso-admin')

    Inline_Policy_change = "arn:aws:s3:::*" + division_value.lower() + "*"

    logger.info('Getting an inline Policy refernce from a permissionSet')

    # TODO : move these variables to a config environment
    # This  code is for the demo purposes only. You can move these variables into a config file

    response = client.get_inline_policy_for_permission_set(
        InstanceArn='arn:aws:sso:::instance/<SSO-Instance>',
        PermissionSetArn='arn:aws:sso:::permissionSet/<SSO-Instance>/<permission policy>',
    )

    logger.info('Loading the inline poilicy before updating it')
    # Load the inline policy
    inlinePolicy = json.loads(response['InlinePolicy'])

    logger.info('Print the inlinePolicy')
    logger.info(inlinePolicy)
    # Load the resources
    resource_extracted = inlinePolicy['Statement']['Resource']

    # Validate if "Divison field" is already present in the inline policy
    if any(division_value in string for string in resource_extracted):
        logger.info('Division already added to the policy No Action needed ')
        # Return the response to workflow if policy is not updated
        return {
            'statusCode': 200,
            'body': json.dumps('Policy not updated, division ' + division_value + ' alreay part of the poilicy')
        }
    else:
        # updating inline policy statement with a new division value
        Inline_Policy_change = "arn:aws:s3:::*" + division_value + "*"
        inlinePolicy['Statement']['Resource'].append(Inline_Policy_change)

    logger.info('Updated Inline policy:')
    logger.info(inlinePolicy)

    # Update the permission set with an updated inline policy
    response = client.put_inline_policy_to_permission_set(
        InstanceArn='arn:aws:sso:::instance/<SSO-Instance>',
        PermissionSetArn='arn:aws:sso:::permissionSet/<SSO-Instance>/<permission policy>',
        InlinePolicy=json.dumps(inlinePolicy))

    logger.info('End of the function')
    logger.info('Returning the response')
    # Return the response to workflow if policy is updated

    return {
        'statusCode': 200,
        'body': json.dumps('Policy updated, division ' + division_value + ' is now a part of the poilicy')
    }
