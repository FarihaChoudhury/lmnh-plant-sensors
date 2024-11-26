"""Transform.py: Clean the data."""
# pylint: disable=line-too-long

import re
import pandas as pd


FILENAME = "Plant_information.csv"
DECIMAL_PLACES = 2
EMAIL_REGEX = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"""
CLEAN_FILENAME = "clean_plant_info.csv"


def load_data(filename: str) -> pd.DataFrame:
    """Create dataframe with plant information collected from API."""
    return pd.read_csv(filename)


def convert_datatypes(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to correct datatypes."""
    dataframe["recording_taken"] = pd.to_datetime(
        dataframe["recording_taken"], format='%Y-%m-%d %H:%M:%S')
    dataframe["last_watered"] = pd.to_datetime(
        dataframe["last_watered"], format='%a, %d %b %Y %H:%M:%S %Z', utc=True)
    dataframe["last_watered"] = pd.to_datetime(dataframe["last_watered"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"))
    return dataframe


def round_floats(dataframe: pd.DataFrame, decimal_places: int) -> pd.DataFrame:
    """Round all float columns to 2 decimal places."""
    cols_to_round = ["longitude", "latitude", "temperature", "soil_moisture"]
    for col in cols_to_round:
        dataframe[col] = dataframe[col].round(
            decimal_places).apply(lambda x: f"{x:.2f}")
    return dataframe


def verify_emails(dataframe: pd.DataFrame, email_regex: str) -> pd.DataFrame:
    """Verify the emails are proper emails using regex."""
    dataframe["email"] = dataframe["email"].apply(
        lambda x: x if re.match(email_regex, x) else None)
    return dataframe


def main_transform(filename: str, decimals: int, regex: str, clean_filename: str) -> pd.DataFrame:
    """Main transform file to clean the data and validate data."""
    plant_metrics_dt = convert_datatypes(load_data(filename))
    plant_metrics_round = round_floats(plant_metrics_dt, decimals)
    plant_metrics = verify_emails(plant_metrics_round, regex)
    return plant_metrics.to_csv(clean_filename)


if __name__ == "__main__":
    main_transform(FILENAME, DECIMAL_PLACES, EMAIL_REGEX, CLEAN_FILENAME)
