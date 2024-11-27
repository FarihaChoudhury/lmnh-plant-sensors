"""Runs the combined functions from extract.py, transform.py and load.py"""

import logging
import asyncio
import pandas as pd
from dotenv import load_dotenv
from extract import fetch_and_collect_data
from transform import convert_datatypes, round_floats, remove_punctuation, verify_emails
from load import get_botanists_id_mapping, get_connection, insert_into_plant_metric

DECIMAL_PLACES = 2
EMAIL_REGEX = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"""


def main() -> None:
    """Runs the main functions for the ETL Pipeline"""
    load_dotenv()

    extracted_data = pd.DataFrame(asyncio.run(fetch_and_collect_data()))

    plant_metrics_dt = convert_datatypes(extracted_data)
    plant_metrics_round = round_floats(plant_metrics_dt, DECIMAL_PLACES)
    plant_metrics = remove_punctuation(
        verify_emails(plant_metrics_round, EMAIL_REGEX))

    try:
        metric_df = plant_metrics

        with get_connection() as conn:
            botanist_names = metric_df['name'].unique().tolist()

            botanist_id_mapping = get_botanists_id_mapping(
                conn, botanist_names)

            insert_into_plant_metric(conn, metric_df, botanist_id_mapping)

    except Exception as e:
        logging.error(
            "An error occurred during the execution of the program: %s", e)


if __name__ == "__main__":
    main()
