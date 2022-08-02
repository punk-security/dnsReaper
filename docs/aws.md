# AWS

The AWS provider connects to AWS and fetches all public zones and then enumerates the records in these zones.

To enumerate Route53 zones, you need to provide an access key id and secret with IAM permissions
to list and get Route53 zones.  This is done through standard switches like all other options.

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