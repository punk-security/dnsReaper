# AWS

## Description
The AWS provider connects to AWS and fetches all public zones and then enumerates the records in these zones.

To enumerate Route53 zones, you need to provide an access key id and secret with IAM permissions
to list and get Route53 zones.  This is done through standard switches like all other options.


## Usage
The command-line options `--aws-access-key-id` and `--aws-access-key-secret` can be used to specify credentials.

If you do not provide these options, the AWS provider will use the following ways of obtaining credentials, in order:
1. Environment variables
2. Shared credential file (~/.aws/credentials)
3. AWS config file (~/.aws/config)
4. Assume Role provider
5. Boto2 config file (/etc/boto.cfg and ~/.boto)
6. Instance metadata service on an Amazon EC2 instance that has an IAM role configured.

For more information, please see the
[boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).

## Requirements
As a minimum you need:
* GetHostedZone
* ListHostedZones
* ListResourceRecordSets

A suggested inline policy for the account would be:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "route53:GetHostedZone",
                "route53:ListHostedZones",
                "route53:ListResourceRecordSets"
            ],
            "Resource": "*"
        }
    ]
}
```