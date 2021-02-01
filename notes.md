# Implementation Notes

Here are some notes on trying out AWS services. Services that are used in this project include:

* Lambda: for event based functionality, such as polling for confirmation, and calling SES
* SES: sending greeting email
* SNS: email/phone subscription, one to many publish message
* EC2: basic flask hosting
* CloudWatch: monitor Lambda test running logs

Note that those ARN string left in the script are not sensitive, calling on those ARN will result in permission error,
if one does not acquire proper AWS credential associated with those resources.

## Problems & Solutions

1. If executing code in sudo, it cannot read the aws credential.
2. By default AWS SES is in the sandbox mode. This means that no emails can go outside the sandbox, to prevent spam to
   other users. Send an application to move out of the sandbox.
3. If the lambda function requires longer execution time, set the timeout longer. The default is 3 seconds.
4. To have lambda call SNS service, configure the execution role in the permission tab.
5. TargetArn: for kindle or mobile phone, not for specific email. SNS does not support sending to specific email.  
   Use SES instead.
6. IAM policy change often takes minutes to take effect. Test immediately after attaching a policy often results in
   permission error. Best plan for policy and resources to be used, and configure in one go.

## Flask Deployment

1. attach an elastic IP to the EC2 instance
2. modify security group setting to allow traffic into the port
3. launch flask application to listen to that port

## Subscription Routine

1. register email on the website
2. send a confirmation email customize email content let AWS Lambda handle the confirmation logic Note that currently
   SNS does not support customized confirmation template.
3. confirm the subscription Use AWS Lambda to poll the confirmation state of the newly subscribed email. When the user
   confirms, send a greeting email by SES.
4. send a welcome email AWS SNS supports email template, write html to make it look prettier.
5. Push actual stuff to the subscribers Using SNS to perform one to many push.


