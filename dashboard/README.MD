# Dashboard

This folder contains all the code, documentation and resources necessary for the Dashboard to run successfully.

## Diagram 📊

### Dashboard Wireframe

![Dashboard Wireframe](/images/wireframe.png)

## Requirements 📋

To run this script and containerize into a docker image, you will need the following:

- **Python**: Version 3.10
- `pytest`: For running unit tests
- `pytest-cov`: For measuring test coverage
- `pandas`: For data manipulation and analysis
- `python-dotenv`: For loading environment variables from a `.env` file
- `pymssql`: For connecting to Microsoft SQL Server
- `streamlit`: For creating an interactive web application for visualisations
- `altair`: For creating declarative statistical visualisations
- `streamlit-autorefresh`: For realtime updates of the graphs.
- `google-generativeai`: For interacting with Google Gemini API.

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

## Files Explained 🗂️
- `Dockerfile` - Containerizes the streamlit and queries, allowing it run in an ECS.
- `streamlit.py` - The main application file for the Streamlit dashboard. It handles the user interface, including filtering options, visualisations, and real-time data rendering for the LNMH Plant Monitoring System.
- `db_queries.py` - Contains database interaction logic for fetching real-time and archival plant metrics. It abstracts queries to simplify data retrieval for visualizations.
- `test_queries.py` - Contains tests for the database queries, ensuring they work and edge cases are covered. Has a x% coverage. 

## Secrets Management 🕵🏽‍♂️

Before running the script, you need to set up your AWS credentials. Create a new file called `.env` in the `dashboard` directory and add the following lines, with your actual AWS keys and database details:

| Variable         | Description                                      |
|------------------|--------------------------------------------------|
| DB_HOST          | The hostname or IP address of the database.      |
| DB_PORT          | The port number for the database connection.     |
| DB_PASSWORD      | The password for the database user.              |
| DB_USER          | The username for the database.                   |
| DB_NAME          | The name of the database.                        |
| SCHEMA_NAME      | The name of the database schema.                 |
| GEMINI_API_KEY   | The Google Gemini API key.                       |


You'll need to register with the Google Gemini Api and create an API KEY to include in your `.env` file.


## AWS Setup and Docker Instructions ⚙️

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
