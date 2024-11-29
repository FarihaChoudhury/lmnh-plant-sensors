# Terraform 🏗️

This directory focuses on **terraforming** all the AWS cloud services that are used throughout the Plants Monitoring application.

## Files Explained 🗂️
* `main.tf` - This file contains the core Terraform configuration, defining the resources and infrastructure to be provisioned in AWS.  
* `variables.tf` - This file acts as a blueprint for all the variables used in the Terraform configuration. It includes the definitions of the variables that store sensitive information, such as AWS credentials, region configurations, and other secret keys that are required for resource creation. 
* `terraform.tfvars` - This file is where the actual values for the variables defined in `variables.tf` are stored.


## Terraformed AWS services 💼
* Lambda - to run the ETL pipeline for extracting plant metrics and uploading to the RDS. 
* Event Bridge schedules - to schedule the ETL pipeline lambda for every minute.
* Lambda - to run the archive process everyday at 12am, moving plant statistics to long term storage.
* Event bridge Schedule - to schedule the archive lambda for every day 12am. 
* ECS Service - to run the dashboard continuously.

## Installation ⚙️

Navigate to the project directory:
```bash
cd terraform
```

## Usage 🔄 
The main script to create AWS cloud services through terraform is `main.tf`. You can run it with the following command:

To initialise: 
```bash
terraform init 
```

To create the services:
```bash
terraform plan
terraform apply 
```
The ```apply``` command will prompt the user to enter ```yes``` to confirm the creation of the services. The services will then be created on AWS unless an error with any credentials has occurred. 

To destroy:
```bash
terraform destroy
```

## Secrets Management 🕵🏽‍♂️

Before running the script, you need to set up your AWS credentials. Create a new file called `.terraform.tfvars` in the `terraform` directory and add the following lines, with your actual AWS keys and database details:

| Variable          | Description                                            |
|-------------------|--------------------------------------------------------|
| AWS_ACCESS_KEY    | The access key for AWS authentication.                 |
| AWS_SECRET_KEY    | The secret key for AWS authentication.                 |
| AWS_REGION        | The AWS region where your resources will be deployed.  |
| C14_VPC           | The VPC (Virtual Private Cloud) ID.                    |
| C14_SUBNET_1      | The subnet id 1.                                       |
| C14_SUBNET_2      | The subnet id 2.                                       |
| C14_SUBNET_3      | The subnet id 3.                                       |
| C14_CLUSTER       | The cluster for the ECS service.                       |
| DB_USER           | The username for the database.                         |
| DB_PASSWORD       | The password for the database user.                    |
| DB_NAME           | The name of the database.                              |
| DB_HOST           | The hostname or IP address of the database.            |
| DB_PORT           | The port number for the database connection.           |
| SCHEMA_NAME       | The name of the database schema.                       |
| ETL_ECR_URI       | The URI for the ETL container repository in ECR.       |
| DASHBOARD_ECR_URI | The URI for the dashboard container repository in ECR. |
| ARCHIVE_ECR_URI   | The URI for the Archive container repository in ECR.   |


