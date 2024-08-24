 terraform { 
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=5.16, <6.0"
    }
  }
 }


### Gets caller's ID
data "aws_caller_identity" "current" {
  # Retrieves information about the AWS account corresponding to the
  # access key being used to run Terraform, which we need to populate
  # the "source_account" on the permission resource.
}

data "aws_region" "region" {}

resource "aws_dynamodb_table" "results" {
  name           = "dnsreaper-results"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "guid"
    type = "S"
  }
  hash_key = "guid"
}

resource "time_static" "src" {
  triggers = {
    src : sha1(join("", [for f in fileset("${path.root}/","*.py"): filesha1(f)]))
  }
}

resource "null_resource" "build_venv" {
  triggers = {
    id = time_static.src.unix
  }

  provisioner "local-exec" {
    command = "docker build -t ${time_static.src.unix} ${path.root} -f ${path.root}/Dockerfile --target lambda && docker create --name ${time_static.src.unix} ${time_static.src.unix} && docker cp ${time_static.src.unix}:/packaged_app.zip ${path.root}/${time_static.src.unix}.zip && docker rm -v ${time_static.src.unix}"
  }
}

### Logs
resource "aws_cloudwatch_log_group" "logs" {
  name              = "/aws/lambda/dnsReaper-public-lambda"
  retention_in_days = 14
}

resource "aws_lambda_function" "serverless-dnsreaper" {
  depends_on    = [ "null_resource.build_venv" ]
  description   = time_static.src.unix
  filename      = "${path.root}/${time_static.src.unix}.zip"
  function_name = "dnsReaper-public-lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler = "lambda.handler"

  runtime = "python3.11"

  timeout = 30
  memory_size = 256

  environment {
    variables = {
      PD_API_KEY = file("./pdkey"),
      DYNAMO_TABLE = aws_dynamodb_table.results.name
      }
  }
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "execution" {
  statement {
    effect = "Allow"
    actions = [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface"        
        ]
    resources = ["*"]
  }
    statement {
    actions = [
      "logs:CreateLogGroup",
    ]
    resources = ["arn:aws:logs:${data.aws_region.region.name}:${data.aws_caller_identity.current.account_id}:*"]
  }
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["${aws_cloudwatch_log_group.logs.arn}:*"]
  }

  statement {
    actions = [
      "dynamodb:PutItem",
      "dynamodb:GetItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem",
      "dynamodb:BatchGetItem",
      "dynamodb:BatchWriteItem",
      "dynamodb:Scan",
      "dynamodb:Query"
    ]
    resources = [aws_dynamodb_table.results.arn]
  }

}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  inline_policy {
    name = "execution_policy"
    policy = data.aws_iam_policy_document.execution.json
  }
}


