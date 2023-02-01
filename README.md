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
  ![Link](https://github.com/sunkara-bhanu/list-instance-by-region/blob/main/img/terraform_tfvars.JPG)
  3. Change the BUCKET_NAME in the file providers.tf with the bucket you created in pre-requisites. Use the bucket name, not the ARN
  4. Change the BUCKET_NAME in the file airbus_dev_devops02_code_repo/lambda_bootstrap/providers.tf with the bucket you created in pre-requisites. Use the bucket name, not the ARN
  5. Change the BUCKET_NAME in the file modules/codepipeline/roles.tf with the bucket you created in pre-requisites. Use the Bucket ARN here.
  6. Navigate to code_pipeline_deployment and run "terraform init"
  7. Run "terraform validate"
  8. Run "terraform plan" and review the output in terminal
  9. Run "terraform apply" and review the output in terminal and when ready, type yes and hit enter
  
 Part#3:
  1. Push the Lambda code to codecommit using codecommit url generated from Part#2 which will trigger codepipeline to deploy the lambda code.
  2. Run cd.. into the Root folder. From the output above, copy the code commit repository link.
  3. Run git clone <codecommit repo link>
      a. If credentials are required, Generate a CodeCommit credentials from aws console for the IAM user that you logged in:
      b. Select Users from IAM (Access Management Tab)
      c. Select the user that you want to provide CodeCommit Access to.
      d. Select Security Credentials from the User information panel.
      e. Scroll down and you should be seeing a subsection HTTPS Git credentials for AWS CodeCommit
      f. Click on Generate Credentials, you should be prompted with Download credentails in cvs file.
  4. Once git clone and git authentication is successful, cd to cloned directory. This directoy will be empty as we haven't pushed the code yet.
  5. Copy Lambda application code from lambda_bootstrap folder to git repo by running cp -R lambda_bootstrap codecommitrepo/ . 
  6. Push the changes to git repo by running git add. && git commit -m "Initial Commit" && git push
  7. Now navigate to AWS Codepipeline from aws console and check the pipeline status as shown below.
  
  ![Link](https://github.com/sunkara-bhanu/list-instance-by-region/blob/main/img/Code_Pipeline_Image.JPG)
  
Part#4:
  1. Navigate to the unit_tests folder from root folder for [Link](https://github.com/sunkara-bhanu/list-instance-by-region/tree/main/unit_tests) 
  2. Run the file from ide with pytest plugin installed
  3. From terminal run "pytest" which will pick the test cases defined in the test_list_instances.py file and summarize the test result.
  
  ![Link](https://github.com/sunkara-bhanu/list-instance-by-region/blob/main/img/Unit_Test_Results.JPG)
  
Part#5:
  1. Open POST man and create new collection with "GET" request type
  2. Copy the API end point generated from Part#3 and also api key resource generated from the api gateway resource
      eg., API end point: https://b423a19tgi.execute-api.ap-south-1.amazonaws.com/dev/list_ec2?instance_region=us-east-1
           API key: HoreP1O2ON1RTKzabsfx61JmrirqyYnE4ROw0Yw1
  3. Use API key under authorization tab and Key as "x-api-key" and value as API key from the previous step
  4. Add the required query parameter instance region with value eg., "all" or specific aws region to the api end point from step#2
      eg., https://b423a19tgi.execute-api.ap-south-1.amazonaws.com/dev/list_ec2?instance_region=us-east-1
  5. Check the API response and status code 
