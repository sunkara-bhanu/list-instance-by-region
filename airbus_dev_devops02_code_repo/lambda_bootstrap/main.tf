data "aws_ecr_image" "lambda_image_latest" {
  repository_name = split("/", var.ecr_repo_url)[1]
  image_tag       = "latest"
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "${var.env_namespace}_lambda_role"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy" "iam_policy_for_lambda" {
  role   = aws_iam_role.iam_for_lambda.name
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "${var.ecr_repo_arn}"
      ],
      "Action": [
        "ecr:*"
      ]
    },
    {
      "Effect": "Allow",
      "Resource": [
        "*"
      ],
      "Action": [
        "ecr:GetAuthorizationToken"
      ]
    },
    {
      "Effect": "Allow",
      "Resource": [
        "arn:aws:logs:${var.region}:${var.account_id}:*"
      ],
      "Action": [
        "logs:CreateLogGroup"
      ]
    },
    {
      "Effect": "Allow",
      "Resource": [
        "arn:aws:logs:${var.region}:${var.account_id}:log-group:/aws/lambda/list_instance_lambda:*"
        ],
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
    },
    {
      "Effect": "Allow",
      "Resource": "*",
      "Action": [
        "ec2:Describe*"
      ]
    }
  ]
}
POLICY
}
resource "aws_lambda_function" "main" {
  function_name    = "${var.env_namespace}_lambda"
  image_uri        = "${var.ecr_repo_url}:latest"
  package_type     = "Image"
  role             = aws_iam_role.iam_for_lambda.arn
  source_code_hash = data.aws_ecr_image.lambda_image_latest.id
  timeout          = 60
}

# API resouces
resource "aws_api_gateway_rest_api" "api"{
    name = "list_instances_by_region"
    endpoint_configuration {
      types = ["REGIONAL"]
    }

}

resource "aws_api_gateway_resource" "resource"{
    parent_id = aws_api_gateway_rest_api.api.root_resource_id
    path_part = "list_ec2"
    rest_api_id = aws_api_gateway_rest_api.api.id
}

resource "aws_api_gateway_method" "method" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.resource.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  api_key_required = true
}

resource "aws_api_gateway_integration" "integration" {
  http_method = aws_api_gateway_method.method.http_method
  resource_id = aws_api_gateway_resource.resource.id
  rest_api_id = aws_api_gateway_rest_api.api.id
  type        = "AWS"
  integration_http_method = "POST"
  uri = aws_lambda_function.main.invoke_arn
    request_templates = {
    "application/json" = <<EOF
{
   "instance_region" : "$input.params('instance_region')"
}
EOF
  }

}

resource "aws_api_gateway_method_response" "response_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.resource.id
  http_method = aws_api_gateway_method.method.http_method
  status_code = "200"
}

resource "aws_api_gateway_integration_response" "integation_response_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.resource.id
  http_method = aws_api_gateway_method.method.http_method
  status_code = aws_api_gateway_method_response.response_200.status_code
  depends_on = [
    aws_api_gateway_integration.integration
  ]
}

resource "aws_api_gateway_method_response" "response_400" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.resource.id
  http_method = aws_api_gateway_method.method.http_method
  status_code = "400"
}

resource "aws_api_gateway_integration_response" "integation_response_400" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.resource.id
  http_method = aws_api_gateway_method.method.http_method
  status_code = aws_api_gateway_method_response.response_400.status_code
  selection_pattern = ".*Error.*"

  # Transforms the backend JSON response to XML
  response_templates = {
    "application/json" = <<EOF
#set ($errorMessageObj = $util.parseJson($input.path('$.errorMessage')))
{
	"code" : "400",
	"message" : "Bad Request"
}
EOF
  }
}

# Lambda
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "arn:aws:execute-api:${var.region}:${var.account_id}:${aws_api_gateway_rest_api.api.id}/*/${aws_api_gateway_method.method.http_method}${aws_api_gateway_resource.resource.path}"
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  triggers = {
    # NOTE: The configuration below will satisfy ordering considerations,
    #       but not pick up all future REST API changes. More advanced patterns
    #       are possible, such as using the filesha1() function against the
    #       Terraform configuration file(s) or removing the .id references to
    #       calculate a hash against whole resources. Be aware that using whole
    #       resources will show a difference after the initial implementation.
    #       It will stabilize to only change when resources change afterwards.
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.resource.id,
      aws_api_gateway_method.method.id,
      aws_api_gateway_integration.integration.id,
      # aws_api_gateway_usage_plan.list_instance_usage_plan.id,
      # aws_api_gateway_usage_plan.list_instance_usage_plan_key.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = "dev"
}

resource "aws_api_gateway_api_key" "list_instance_key" {
  name = "List_instance_api_key"
}

resource "aws_api_gateway_usage_plan" "list_instance_usage_plan" {
  name = "list_instance_usage_plan"

  api_stages {
    api_id = aws_api_gateway_rest_api.api.id
    stage  = aws_api_gateway_stage.stage.stage_name
  }
}

resource "aws_api_gateway_usage_plan_key" "list_instance_usage_plan_key" {
  key_id        = aws_api_gateway_api_key.list_instance_key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.list_instance_usage_plan.id
}