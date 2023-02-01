provider "aws" {
  region = "ap-south-1"
}

terraform {
    backend "s3" {
      encrypt = true
      bucket = "list-instance-terraform-state"
      key = "states/lambda/terraform.tfstate"
      region = "ap-south-1"
  }
}
