#Amazon S3 Bucket New User Welcome Email Generation
from __future__ import print_function
import sys
import boto3
import json
import collections

#Define S3 Bucket
bucket = "BUCKET_NAME"

#Define DynamoDB Table Name
table_name = "Lambda-AD-New-User-Email-GUID"

#Define SES Global Email Parameters
email_from = 'EMAIL_FROM'
email_subject = 'EMAIL_SUBJECT'
email_body_text = 'EMAIL_BODY_TEXT'
email_body_html = 'EMAIL_BODY_HTML'

#Connect to S3 with Boto3
s3 = boto3.client('s3')

#Connect to DynamoDB with Boto3
db = boto3.client('dynamodb')

#Connect to SES with Boto3
ses = boto3.client('ses')

def lambda_handler(event, context):
    #Find Most Recently Modified Active Users File from S3
    bucket_list = s3.list_objects(Bucket=bucket).get('Contents', [])
    print(bucket_list)

    for file in bucket_list:
        file_name = file['Key']

        try:
            object = s3.get_object(Bucket=bucket,Key=file_name)['Body']

        except Exception, e:
            print ("Error Encountered while downloading file.")
            print (e)
            exit()

        users = json.load(object)

        #Send Welcome Email to New User
        print("****Sending Welcome Emails****")
        
        for user in users:
            user_name = user['DisplayName']
            user_email = user['EmailAddress']
            user_guid = user['objectGUID']

       try:
            object = s3.get_object(Bucket=bucket,Key=file_name)['Body']

        except Exception, e:
            print ("Error Encountered while downloading file.")
            print (e)
            exit()

        users = json.load(object)

        #Send Welcome Email to New User
        print("****Sending Welcome Emails****")
        
        for user in users:
            user_name = user['DisplayName']
            user_email = user['EmailAddress']
            user_guid = user['objectGUID']

            try:
                response = db.get_item(
                    TableName= table_name,
                    Key={
                        'GUID': {
                            'S': user_guid
                        }
                    },
                    ConsistentRead=True
                )
            except:
                print("Error in DynamoDB item fetch.")
            
            dynamo_GUID = json.dumps(response)
            
            if user_guid in dynamo_GUID:
                print("Found GUID: %s" % dynamo_GUID)
            else:
                print("User %s %s not found.  Sending Welcome Email" % (user_name, user_email))
                response = ses.send_email(
    		        Source = email_from,
    		        Destination={
    		            'ToAddresses': [
    		                user_email,
    		            ],
    		        },
    		        Message={
    		            'Subject': {
    		                'Data': email_subject
    		            },
    		            'Body': {
    		                'Text': {
    		                    'Data': email_body_text
    		                },
                        'Html': {
    		                	'Data': email_body_html
    		                }
    		            }
    		        }
    		    )

                response = db.put_item(
                    TableName= table_name,
                    Item={
                        'GUID': {
                            'S': user_guid
                        },
                        'User_Name': {
                            'S': user_name
                        },
                        'Email_Address': {
                            'S': user_email
                        }
                    }
                )
    print("Deleting File")
    s3.delete_object(Bucket=bucket,Key=file_name)
