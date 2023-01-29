terraform{
    backend "s3" {
        bucket = "list-instance-terraform-state"
        encrypt = true
        key = "terraform.tfstate"
        region = "ap-south-1"
    }
}

provider "aws" {
    region = "ap-south-1"
}