"""Runs the combined functions from extract.py, transform.py and load.py"""

# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long

from dotenv import load_dotenv
from extract import main as extract
from transform import main as transform
from load import main as load


def lambda_handler(event, context):
    """Runs the ETL pipeline when the lambda is invoked"""
    try:
        main()
        return {
            "statuscode": 200,
            "body": "ETL pipeline executed successfully!"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"An unexpected error occurred: {e}"
        }


def main() -> None:
    """
    Executes the ETL (Extract, Transform, Load) pipeline for plant metrics.

    1. Extract: Fetching and collecting plant data asynchronously from an external API.
    2. Transform: Cleaning, verifying, and transforming the data
    3. Load: Storing the transformed data into a database
    """
    load_dotenv()

    extracted_plants_metrics = extract()

    cleaned_plant_metrics = transform(extracted_plants_metrics)

    load(cleaned_plant_metrics)


if __name__ == "__main__":
    main()
