# Lambda-AD-New-User-Email
Send new active directory users a welcome email

The purpose of this project is to send new Active Directory users a welcome email.  The methodology will rely upon the following:
  - Powershell Script to Retrieve Active Directory users and Details to a JSON file
  - Put the Active Directory user details to a specified S3 bucket
  - Lambda function to check objectCreated date against the last time the process was run, stored in DynamoDB

Requirements
  - AWS Lambda Environment (Python 2.7)
  - AWS S3 Bucket
  - AWS Tools for Windows PowerShell installed on Domain Controller (https://aws.amazon.com/powershell/)
  - PowerShell v3 or above set to Unrestricted execution mode
  - Boto3 AWS SDK for Python (https://github.com/boto/boto3)

Legacy Servers may upgrade PowerShell to v3 by installing .NET Framework 4.5 and the Windows Management Framework 3.0 here:
  - Windows 2008 R2: https://www.microsoft.com/en-us/download/confirmation.aspx?id=34595&6B49FDFB-8E5B-4B07-BC31-15695C5A2143=1

  - Windows 2008 (64-bit): https://download.microsoft.com/download/E/7/6/E76850B8-DA6E-4FF5-8CCE-A24FC513FD16/Windows6.0-KB2506146-x64.msu

Installation (Lambda)
  - Create an AWS S3 bucket
  - Create a DynamoDB take named Lambda-AD-New-User-Email-GUID with Primary Key "GUID" and Read and Write capacities of "1" (As of Feb 2016 about $0.59 per month)
  - Upload Lambda-New-User.py to an AWS Lambda Python 2.7 function
  - Name your Lambda function handler Lambda-2-Zendesk.lambda_handler
  - Choose S3 Execution Role, Create a new IAM role, and set the execution policy to the IAM POLICY document in the Lambda project folder
  - Set Lambda function timeout to 300 seconds
  - Set Event Source to the S3 bucket for ObjectCreated | json
  - (Optional) Set Event Source to S3 bucket for rate(1 hour)

Installation (Windows)
  - Install AWS Tools for Windows PowerShell
  - Create AWS IAM User with IAM POLICY document in the LDAP-2-S3 project folder
  - Download and modify AD-2-S3.ps1 to include S3 bucket Access Key, Secret Key, and Bucket
  - Schedule AD-2-S3.ps1 to run using Windows Task Scheduler or preferred RMM tool
