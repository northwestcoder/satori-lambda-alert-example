terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

 
data "archive_file" "zip_the_python_code" {
type        = "zip"
source_dir  = "${path.module}/src/"
output_path = "${path.module}/lambda-python.zip"
}
 
resource "aws_lambda_function" "satori_terraform_lambda_func" {
filename                       = "${path.module}/lambda-python.zip"
source_code_hash               = "${data.archive_file.zip_the_python_code.output_base64sha256}"
function_name                  = "Satori_Lambda_Function"
role                           = aws_iam_role.lambda_role.arn
handler                        = "lambda.lambda_handler"
runtime                        = "python3.8"
timeout                        = 120
depends_on                     = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
layers                         = ["arn:aws:lambda:us-east-1:336392948345:layer:AWSDataWrangler-Python38:8"]
}
