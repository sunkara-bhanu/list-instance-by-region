# List EC2 instance by region
This project lists resources required to fetch instances across available aws regions

Below are the steps covered to launch resources,
1. Launch instances using terraform script selecting the region in which you like to deploy the resources
![Launch Instance](https://github.com/sunkara-bhanu/list-instance-by-region/blob/main/img/Launch_Instance.JPG)

2. Deploy code pipe line resources ie., code commit, code build, ECR, code pipeline resources to enable CI/CD capability.

3. Retrieve the code commit repo from step#2 and add the resources that requires CI/CD flow (eg., API Gateway and Lambda resources).  

![Deploy Pipeline resources](https://github.com/sunkara-bhanu/list-instance-by-region/blob/main/img/CI_CD_Apigateway_Lambda_Resources.JPG)

4. Perform unit testing of the rest end point generated from step#3 

5. Invoke rest  end point generated from step#3 with valid parameters to retrieve the instances across regions

![Fetch instances](https://github.com/sunkara-bhanu/list-instance-by-region/blob/main/img/Fetch_Instance_Info_Through_API.JPG)

Pre-requisites
Install Terraform : [Link] (https://developer.hashicorp.com/terraform/downloads)
Install AWS CLI : [Link] (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 
Configure AWS CLI with AWS Account do aws sts get-caller-identity for validation) : [Link] (https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
Create a S3 Bucket in ap-south-1. This bucket will be used to store the terraform state file. Note the bucket arn as it will be used in the steps below.

This code is split into 5 parts,

Part#1:
  1. Infrastructure for launching instnaces can be found in [Link](https://github.com/sunkara-bhanu/list-instance-by-region/tree/main/deploy_instances)
  2. Navigate to the folder deploy_instances and run "terraform init" in the terminal
  3. Run command "terraform apply -var="input_region=ap-south-1" -auto-approve" to deploy the resource in region ap-south-1. You can use any region with in ap-xxx.
  4. Public ip of the created instance will be shown as output, which can be used to validate the instance deployment in region specified
  5. Run command "terraform destroy -var="input_region=ap-south-1" -auto-approve" to delete the resources created.
  
Part#2:
  1. Deploy infrastructure for Codepipeline Deployment can be found in [Link](https://github.com/sunkara-bhanu/list-instance-by-region/tree/main/code_pipeline_deployment)
  2. Navigate to folder code_pipeline_deploymen and change the ORG_NAME, TEAM_NAME and PROJECT_ID. values from terraform.tfvars
  ![Link]()
  
  
  3. Change the BUCKET_NAME in the file providers.tf with the bucket you created in pre-requisites. Use the bucket name, not the ARN
  4. Change the BUCKET_NAME in the file airbus_dev_devops02_code_repo/providers.tf with the bucket you created in pre-requisites. Use the bucket name, not the ARN
  5. Change the BUCKET_NAME in the file modules/codepipeline/roles.tf with the bucket you created in pre-requisites. Use the Bucket ARN here.
  

