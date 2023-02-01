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

