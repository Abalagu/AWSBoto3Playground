# Created by Luming on 1/31/2021 8:37 PM
import json
import time

import boto3


def subscribe(sns_client, email: str):
    response = sns_client.subscribe(
        TopicArn='arn:aws:sns:us-east-2:174995164214:FlaskPushSNS',
        Protocol='email',
        Endpoint=email,
        ReturnSubscriptionArn=True
    )
    return response


def poll_pending_subscription(sns_client, SubscriptionArn: str):
    pending = True
    count = 0
    while pending:
        attr = sns_client.get_subscription_attributes(SubscriptionArn=SubscriptionArn)
        if attr['Attributes']['PendingConfirmation'] == 'false':
            pending = False
        else:
            print('{}: wait for confirmation'.format(count))
            count += 1
            time.sleep(10)
    else:
        print('subscribed! Arn: {}'.format(SubscriptionArn))


def lambda_handler(event, context):
    sns_client = boto3.client('sns')
    email = event['email']
    response = subscribe(sns_client, email)
    poll_pending_subscription(sns_client, response['SubscriptionArn'])

    payload = json.dumps({'email': email, 'arn': response['SubscriptionArn']})
    """call another function to send the email"""
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(
        FunctionName='GreetingNewSubscriber', InvocationType='Event', Payload=payload
    )
    print('another lambda function invoked to handle sending greeting email')
    return
