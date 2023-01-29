resource "aws_s3_bucket" "codepipeline_artifacts" {
  bucket = "list-instance-pipeline-artifacts"
  acl    = "private"
  
} 