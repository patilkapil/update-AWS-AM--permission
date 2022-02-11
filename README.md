# update-AWS-AM--permission
Code in this repo updates the IAM permission policy via an AWS Lambda function.

# Description 
The sample demonstrates how to update IAM inline permission policies. This example will demonstrate how can you access and update permission policies without any manual intervention.

# Assumption 
1- Code assumes you have a permission policy and an inline policy 
2- Code will only add/update the resources section of your inline policy


# Python Dependencies
You don't need to install any external dependencies for this AWS Lambda code. 

# Key Considerations
1- Code is for POC/introduction purposes only. For demonstration purposes, I have used hard-coded values. Please refer to Python's best programming practice if you reuse the code.

2- Code is assuming you will get the input in the form of a JSON stirng :

```
  {'division':'<value>'}

```

  
