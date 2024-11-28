# Archive

This folder contains all the code, documentation and resources necessary for the successful migration of data to the archival data storage.

## Requirements

To run this script and containerize into a docker image, you will need the following:

- **Python**: Version 3.10
- `pylint`: For measuring code quality
- `pytest`: For running unit tests
- `pytest-cov`: For measuring test coverage
- `python-dotenv`: For loading environment variables from a `.env` file
- `pymssql`: For connecting to Microsoft SQL Server

To make `pymsql` work, make sure you have the following:

```zsh
brew install sqlcmd
```
```zsh
brew install freetds
```

To install these dependencies, use the following command:

```zsh
pip3 install -r requirements.txt
```

## Files Explained
- `Dockerfile` - Containerizes the archive pipeline to be pushed onto an ECR for the AWS Lambda.
- `archive.py` - The main script that archives plant metric data from the last 24 hours into an archive table in the database. It performs the following:

    - Connects to a Microsoft SQL Server database using credentials stored in environment variables.
    - Retrieves all plant IDs from the database.
    - Calculates the average temperature, soil moisture, and watering count for each plant over the last 24 hours.
    - Archives this data into the plants_archive table.
    - Clears all data from the plant_metric table after archiving.
    - Logs the status of operations to facilitate debugging.
    - Contains a lambda_handler function for AWS Lambda integration.

## Secrets Management

‼️ **Same `.env` file and secrets as pipeline** ‼️

## AWS Setup and Docker Instructions

To set up the AWS environment and build the Docker container, follow these steps:

1. **Create an ECR Repository**:
   - Go to the [AWS Management Console](https://aws.amazon.com/console/) and open the **Elastic Container Registry (ECR)** service.
   - Create a new repository for your Docker image.

2. **Build the Docker Image**:
   - Build the Docker image with the following command, specifying the `linux/amd64` platform:
     ```sh
     docker build --platform linux/amd64 -t your-image-name .
     ```

3. **Login to AWS ECR**:
   - After creating the repository in ECR, follow the instructions in the **Amazon ECR Console** to authenticate Docker to your Amazon ECR. The command typically looks like:
     ```sh
     aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
     ```

4. **Tag and Push the Docker Image to ECR**:
   - Tag your Docker image to match your ECR repository:
     ```sh
     docker tag your-image-name:latest your-account-id.dkr.ecr.your-region.amazonaws.com/your-repository-name:latest
     ```
   - Push the image to your ECR repository:
     ```sh
     docker push your-account-id.dkr.ecr.your-region.amazonaws.com/your-repository-name:latest
     ```

This will upload your Docker image to AWS ECR, making it available for deployment and use in the cloud.