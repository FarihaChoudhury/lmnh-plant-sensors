# Pipeline

This directory contains all the necessary code and documentation for the Extract Transform Load (ETL) pipeline used to collect, clean and upload the data collected from LNMH's Plant Monitoring array.

## Requirements

To run this script, you will need the following:

- **Python**: Version 3.8 or higher
- `pytest`: For running unit tests
- `pytest-cov`: For measuring test coverage
- `requests`: For making HTTP requests
- `pandas`: For data manipulation and analysis
- `python-dotenv`: For loading environment variables from a `.env` file
- `pymssql`: For connecting to Microsoft SQL Server
- `aiohttp`: For asynchronous HTTP requests
- `certifi`: For secure SSL/TLS connections
- `asyncio`: For asynchronous programming
- `pytest-asyncio`: For testing asynchronous code

To make `pymsql` work, you will need the following command:

```zsh
brew install sqlcmd
```

To install these dependencies, use the following command:

```zsh
pip3 install -r requirements.txt
```



## Files Explained
- `etl.py` - Runs the whole ETL pipeline, from extract to loading to rds.
- `extract.py` - establishes a connection to the Heroku API to extract plant metrics data generated every minute, ensuring seamless data retrieval for further processing.
- `test_extract.py` - this test file employs patching techniques to mock external dependencies and validate the functionality of `extract.py`, including the correct extraction of plant metrics, while preventing any real-world API calls. Has a 71% test coverage.
- `transform.py` - this file performs data cleaning tasks, such as removing null values, converting columns to appropriate data types, and ensuring numerical consistency by rounding values to predefined precision levels.
- `test_transform.py` - this test file verifies the main functions in `transform.py` through unit tests, achieving 74% test coverage with pytest, and ensuring that data transformation is performed accurately without introducing errors.
- `load.py` - this file loads takes clean data from transform and loads it into the Microsoft SQL Server hosted on RDS AWS.
- `test_load.py` - this test file verifies the core functions in `load.py` through unit tests.
- `schema.sql` - this SQL script establishes a relational database structure within a specified schema to store and manage plant-related information. Known data is seeded to the tables.
- `reset.sh` - this bash script loads environment variables and utilises them in the running of `schema.sql` in order to create a Microsoft SQL Server database.
- `connect.sh` - this bash script loads environment variables to connect to the created Microsoft SQL Server database.

## Secrets Management
Before running the script, you need to set up your AWS credentials. Create a new file called `.env` in the `pipeline` directory and add the following lines, with your actual AWS keys and database details:

| Variable         | Description                                      |
|------------------|--------------------------------------------------|
| AWS_ACCESS_KEY   | The access key for AWS authentication.           |
| AWS_SECRET_KEY   | The secret key for AWS authentication.           |
| DB_HOST          | The hostname or IP address of the database.      |
| DB_PORT          | The port number for the database connection.     |
| DB_PASSWORD      | The password for the database user.              |
| DB_USER          | The username for the database.                   |
| DB_NAME          | The name of the database.                        |
| SCHEMA_NAME      | The name of the database schema.                 |
| ETL_ECR_URI      | The URI for the ETL container repository in ECR. |
