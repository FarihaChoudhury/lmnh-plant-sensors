"""Transform.py: Clean the data."""
# pylint: disable=line-too-long

import re
import pandas as pd


FILENAME = "Plant_information.csv"
DECIMAL_PLACES = 2
EMAIL_REGEX = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"""
CLEAN_FILENAME = "clean_plant_info.csv"


def convert_datatypes(plants_metrics: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to correct datatypes."""
    plants_metrics["recording_taken"] = pd.to_datetime(
        plants_metrics["recording_taken"], format='%Y-%m-%d %H:%M:%S')
    plants_metrics["last_watered"] = pd.to_datetime(
        plants_metrics["last_watered"], format='%a, %d %b %Y %H:%M:%S %Z', utc=True)
    plants_metrics["last_watered"] = pd.to_datetime(plants_metrics["last_watered"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"))
    return plants_metrics


def round_floats(plants_metrics: pd.DataFrame, decimal_places: int) -> pd.DataFrame:
    """Round all float columns to 2 decimal places."""
    cols_to_round = ["longitude", "latitude", "temperature", "soil_moisture"]
    for col in cols_to_round:
        plants_metrics[col] = plants_metrics[col].round(decimal_places).apply(
            lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
    return plants_metrics


def verify_emails(plants_metrics: pd.DataFrame, email_regex: str) -> pd.DataFrame:
    """Verify the emails are proper emails using regex."""
    plants_metrics["email"] = plants_metrics["email"].apply(
        lambda x: x if re.match(email_regex, x) else None)
    return plants_metrics


def remove_punctuation(plants_metrics: pd.DataFrame):
    """Function to remove extra punctuation from specific columns."""

    columns = ["name", "plant_name", "plant_scientific_name"]
    for col in columns:
        if plants_metrics[col].dtype == 'object':
            plants_metrics[col] = plants_metrics[col].str.replace(
                r"[\"',]", "", regex=True)
    return plants_metrics


def check_for_null_vals(plants_metrics: pd.DataFrame):
    """Check for any null values, discard row if found."""
    plants_metrics["soil_moisture"] = pd.to_numeric(
        plants_metrics["soil_moisture"], errors='coerce')
    plants_metrics["temperature"] = pd.to_numeric(
        plants_metrics["temperature"], errors='coerce')

    return plants_metrics.dropna(subset=["soil_moisture", "temperature", "plant_id", "name"])


def main(extracted_plants_data: list[dict]) -> pd.DataFrame:
    """Cleans the plant readings and validate the data. Returns cleaned data as a Pandas dataframe."""
    plant_metrics_dt = convert_datatypes(extracted_plants_data)
    plant_metrics_round = round_floats(plant_metrics_dt, DECIMAL_PLACES)
    transformed_plant_metrics = remove_punctuation(
        verify_emails(plant_metrics_round, EMAIL_REGEX))
    return transformed_plant_metrics
