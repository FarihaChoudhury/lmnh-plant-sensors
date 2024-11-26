# Terraform 

This directory focuses on **terraforming** all the AWS cloud services that are used throughout the Plants Monitoring application.

## Files Explained
* `main.tf` - contains terraform code to create AWS resources
* `variables.tf` - contains definitions of secrets required to create resources
* `terraform.tfvars` - required to be created, stores secrets from `variables.tf`


## Terraformed AWS services:
* Lambda - to run the ETL pipeline for extracting plant metrics and uploading to the RDS. 
* Event Bridge schedules - to schedule the ETL pipeline lambda for every minute.
* Lambda - to run the archive process everyday at 12am, moving plant statistics to long term storage.
* Event bridge Schedule - to schedule the archive lambda for every day 12am. 
  

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

```text
AWS_ACCESS_KEY=""
AWS_SECRET_KEY=""

C14_VPC=""

DB_HOST=""
DB_PORT=""
DB_PASSWORD=""
DB_USER=""
DB_NAME=""
SCHEMA_NAME=""

ETL_ECR_URI=""
ARCHIVE_ECR_URI=""
```
