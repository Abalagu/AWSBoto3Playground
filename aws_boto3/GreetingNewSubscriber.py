# Created by Luming on 1/31/2021 8:37 PM
import json
import boto3


def lambda_handler(event, context):
    ses_client = boto3.client('ses')
    ses_client.send_email(
        Source='src@gmail.com',  # should be validated in SES
        Destination={
            'ToAddresses': [
                event['email']
            ]
        },
        Message={
            'Subject': {'Data': 'Greeting from AWS Lambda calling SES script'},
            'Body': {'Text': {
                'Data': 'Hello this is the body of the mail. This signifies that you''ve successfully registered. '
                        'Nothing else.'}}
        }
    )
    print('email sent to {}'.format(event['email']))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
