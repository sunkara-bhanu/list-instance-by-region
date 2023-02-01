variable "env_namespace" {
    type = string
    description = "Value is coming from tfvars file that is being updated by buildspec environment variables"
}
variable "ecr_repo_url" {
    type = string
    description = "Value is coming from tfvars file that is being updated by buildspec environment variables"
}
variable "ecr_repo_arn" {
    type = string
    description = "Value is coming from tfvars file that is being updated by buildspec environment variables"
}

variable "account_id" {
  type = number
  default = 534346356116
}

variable "region" {
  type = string
  default = "ap-south-1"
}