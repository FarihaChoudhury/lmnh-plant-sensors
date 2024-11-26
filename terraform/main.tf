provider "aws" {
    region      = var.AWS_REGION
    access_key  = var.AWS_ACCESS_KEY
    secret_key  = var.AWS_SECRET_KEY
}

data "aws_vpc" "c14-vpc" {
    id = "vpc-0344763624ac09cb6"
}

data "aws_subnet" "c14-subnet-1" {
  id = "subnet-0497831b67192adc2"
}

data "aws_subnet" "c14-subnet-2" {
  id = "subnet-0acda1bd2efbf3922"
}

data "aws_subnet" "c14-subnet-3" {
  id = "subnet-0465f224c7432a02e"
}



# --------------- PLANTS ETL: LAMBDA & EVENT BRIDGE

# IAM Role for Lambda execution
resource "aws_iam_role" "c14-runtime-terrors-plants-lambda_execution_role-tf" {
  name = "c14-runtime-terrors-plants-lambda_execution_role-tf"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for Lambda execution role
resource "aws_iam_role_policy" "c14-runtime-terrors-plants-lambda_execution_policy-tf" {
  name = "c14-runtime-terrors-plants-lambda_execution_policy-tf"
  role = aws_iam_role.c14-runtime-terrors-plants-lambda_execution_role-tf.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action   = "dynamodb:Query"
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_lambda_function" "c14-runtime-terrors-plants-etl-lambda-function-tf" {
  role          = aws_iam_role.c14-runtime-terrors-plants--lambda_execution_role-tf.arn
  function_name = "c14-runtime-terrors-plants--etl-lambda-function-new-tf"
  package_type  = "Image"
  architectures = ["x86_64"]
  image_uri     = var.ETL_ECR_URI

  timeout       = 720
  depends_on    = [aws_cloudwatch_log_group.lambda_log_group]

  environment {
    variables = {
      ACCESS_KEY_ID     = var.AWS_ACCESS_KEY,
      SECRET_ACCESS_KEY = var.AWS_SECRET_KEY,
      DB_HOST           = var.DB_HOST,
      DB_NAME           = var.DB_NAME,
      DB_USER           = var.DB_USER,
      DB_PASSWORD       = var.DB_PASSWORD,
      DB_PORT           = var.DB_PORT,
      SCHEMA_NAME       = var.SCHEMA_NAME
    }
  }
    logging_config {
    log_format = "Text"
    log_group  = "/aws/lambda/c14-runtime-terrors-plants-etl-lambda-function-tf"
  }

  tracing_config {
    mode = "PassThrough"
  }
}

# Event bridge schedule: 
# IAM Role for AWS Scheduler
resource "aws_iam_role" "c14-runtime-terrors-plants-etl-scheduler_execution_role-tf" {
  name = "c14-runtime-terrors-plants-etl-scheduler_execution_role-tf"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "c14-runtime-terrors-plants-etl-scheduler_execution_policy-tf" {
  name = "c14-runtime-terrors-plants-etl-scheduler_execution_policy-tf"
  role = aws_iam_role.c14-runtime-terrors-plants-etl-scheduler_execution_role-tf.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "lambda:InvokeFunction"
        Effect   = "Allow"
        Resource = aws_lambda_function.c14-runtime-terrors-plants-etl-lambda-function-tf.arn
      }
    ]
  })
}

# AWS Scheduler Schedule
resource "aws_scheduler_schedule" "c14-runtime-terrors-plants-etl-schedule-tf" {
  name                         = "c14-runtime-terrors-plants-etl-schedule-tf"
  schedule_expression          =  "cron(* * * * ? *)"
  schedule_expression_timezone = "Europe/London"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.c14-runtime-terrors-plants-etl-lambda-function-tf.arn
    role_arn = aws_iam_role.c14-runtime-terrors-plants-etl-scheduler_execution_role-tf.arn
  }
}
