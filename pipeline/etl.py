"""Runs the combined functions from extract.py, transform.py and load.py"""

import logging
import asyncio
import pandas as pd
from dotenv import load_dotenv
from extract import main as extract
from transform import main as transform
from load import main as load
# from load import get_botanists_id_mapping, get_connection, insert_into_plant_metric

DECIMAL_PLACES = 2
EMAIL_REGEX = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"""


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
