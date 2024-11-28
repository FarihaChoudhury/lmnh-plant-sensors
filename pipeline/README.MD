# Pipeline

This directory contains all the necessary code and documentation for the Extract Transform Load (ETL) pipeline used to collect, clean and upload the data collected from LNMH's Plant Monitoring array.

## Requirements

To run this script and containerize into a docker image, you will need the following:

> ⚠️ **Warning**: Make sure you **do not have `asyncio`** or the AWS lambda will not work. ⚠️

- **Python**: Version 3.10
- `pytest`: For running unit tests
- `pytest-cov`: For measuring test coverage
- `requests`: For making HTTP requests
- `pandas`: For data manipulation and analysis
- `python-dotenv`: For loading environment variables from a `.env` file
- `pymssql`: For connecting to Microsoft SQL Server
- `aiohttp`: For asynchronous HTTP requests
- `certifi`: For secure SSL/TLS connections
- `pytest-asyncio`: For testing asynchronous code

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
- `Dockerfile` - Containerizes the ETL pipeline to be pushed onto an ECR.
- `etl.py` - Runs the whole ETL pipeline, from extract to loading to rds, contains lambda_handler for the lambda on AWS.
- `extract.py` - establishes a connection to the Heroku API to extract plant metrics data generated every minute, ensuring seamless data retrieval for further processing.
- `transform.py` - this file performs data cleaning tasks, such as removing null values, converting columns to appropriate data types, and ensuring numerical consistency by rounding values to predefined precision levels.
- `load.py` - this file loads takes clean data from transform and loads it into the Microsoft SQL Server hosted on RDS AWS.

- `schema.sql` - this SQL script establishes a relational database structure within a specified schema to store and manage plant-related information. Known data is seeded to the tables.
- `reset.sh` - this bash script loads environment variables and utilises them in the running of `schema.sql` in order to create a Microsoft SQL Server database.
- `connect.sh` - this bash script loads environment variables to connect to the created Microsoft SQL Server database.

- `test_extract.py` - this test file employs patching techniques to mock external dependencies and validate the functionality of `extract.py`, including the correct extraction of plant metrics, while preventing any real-world API calls. Has a 71% test coverage.
- `test_transform.py` - this test file verifies the main functions in `transform.py` through unit tests, achieving 74% test coverage with pytest, and ensuring that data transformation is performed accurately without introducing errors.
- `test_load.py` - this test file verifies the core functions in `load.py` through unit tests.


## Secrets Management
Before running the script, you need to set up your AWS credentials. Create a new file called `.env` in the `pipeline` directory and add the following lines, with your actual AWS keys and database details:

| Variable         | Description                                      |
|------------------|--------------------------------------------------|
| DB_HOST          | The hostname or IP address of the database.      |
| DB_PORT          | The port number for the database connection.     |
| DB_PASSWORD      | The password for the database user.              |
| DB_USER          | The username for the database.                   |
| DB_NAME          | The name of the database.                        |
| SCHEMA_NAME      | The name of the database schema.                 |

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
