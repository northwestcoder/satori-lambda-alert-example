resource "aws_cloudwatch_event_rule" "satori-lambda" {
  name                  = "satori-run-lambda-function"
  description           = "Schedule lambda function"
  schedule_expression   = "rate(15 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda-function-target" {
  target_id = "lambda-function-target"
  rule      = aws_cloudwatch_event_rule.satori-lambda.name
  arn       = aws_lambda_function.satori_terraform_lambda_func.arn
  input     = <<JSON
    {
      "tag": "custom_classifier"
    }
    JSON

}


resource "aws_lambda_permission" "allow_cloudwatch" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.satori_terraform_lambda_func.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.satori-lambda.arn
}