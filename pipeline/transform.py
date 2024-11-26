"""Transform.py: Clean the data."""

import pandas as pd


FILENAME = "Plant_information.csv"
DECIMAL_PLACES = 2


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
        dataframe[col] = dataframe[col].round(decimal_places)
    return dataframe


if __name__ == "__main__":
    plant_metrics = convert_datatypes(load_data(FILENAME))
    plant_metrics = round_floats(plant_metrics, DECIMAL_PLACES)
