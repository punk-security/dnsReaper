from .templates.cname_found_but_NX_DOMAIN import cname_found_but_NX_DOMAIN

cnames = [
    ".us-east-1.elasticbeanstalk.com",
    ".us-east-2.elasticbeanstalk.com",
    ".us-west-2.elasticbeanstalk.com",
    ".af-south-1.elasticbeanstalk.com",
    ".ap-east-1.elasticbeanstalk.com",
    ".ap-southeast-3.elasticbeanstalk.com",
    ".ap-south-1.elasticbeanstalk.com",
    ".ap-northeast-3.elasticbeanstalk.com",
    ".ap-northeast-2.elasticbeanstalk.com",
    ".ap-northeast-1.elasticbeanstalk.com",
    ".ca-central-1.elasticbeanstalk.com",
    ".eu-central-1.elasticbeanstalk.com",
    ".eu-west-1.elasticbeanstalk.com",
    ".eu-west-2.elasticbeanstalk.com",
    ".eu-south-1.elasticbeanstalk.com",
    ".eu-west-2.elasticbeanstalk.com",
    ".eu-west-3.elasticbeanstalk.com",
    ".eu-north-1.elasticbeanstalk.com",
    ".me-south-1.elasticbeanstalk.com",
    ".sa-east-1.elasticbeanstalk.com",
]

test = cname_found_but_NX_DOMAIN(
    cname=cnames,
    service="AWS Elastic Beanstalk",
)
