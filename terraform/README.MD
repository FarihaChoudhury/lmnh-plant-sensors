# Terraform 

This directory focuses on **terraforming** all the AWS cloud services that are used throughout the Plants Monitoring application.

## Files Explained
* `main.tf` - contains terraform code to create AWS resources
* `variables.tf` - contains definitions of secrets required to create resources
* `terraform.tfvars` - required to be created, stores secrets from `variables.tf`


## Terraformed AWS services:
* Lambda - to run the ETL pipeline for extracting plant metrics and uploading to the RDS. 
* Event Bridge schedules - to schedule the ETL pipeline lambda for every minute.
* ECS Service - to run the dashboard continuously.
  

## Installation

Navigate to the project directory:
```bash
cd terraform
```

## Usage
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

## Secrets Management

Before running the script, you need to set up your AWS credentials. Create a new file called `.terraform.tfvars` in the `terraform` directory and add the following lines, with your actual AWS keys and database details:

| Variable          | Description                                            |
|-------------------|--------------------------------------------------------|
| AWS_ACCESS_KEY    | The access key for AWS authentication.                 |
| AWS_SECRET_KEY    | The secret key for AWS authentication.                 |
| C14_VPC           | The VPC (Virtual Private Cloud) ID.                    |
| C14_SUBNET_1      | The subnet id 1.                                       |
| C14_SUBNET_2      | The subnet id 2.                                       |
| C14_SUBNET_3      | The subnet id 3.                                       |
| C14_CLUSTER       | The cluster for the ECS service.                       |
| DB_HOST           | The hostname or IP address of the database.            |
| DB_PORT           | The port number for the database connection.           |
| DB_PASSWORD       | The password for the database user.                    |
| DB_USER           | The username for the database.                         |
| DB_NAME           | The name of the database.                              |
| SCHEMA_NAME       | The name of the database schema.                       |
| ETL_ECR_URI       | The URI for the ETL container repository in ECR.       |
| DASHBOARD_ECR_URI | The URI for the dashboard container repository in ECR. |

