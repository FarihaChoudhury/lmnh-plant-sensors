"""queries.py: data retrieval for dashboard visualisations."""
# pylint: disable = no-name-in-module

from os import environ
import pandas as pd
from pymssql import Cursor


def get_latest_metrics(cursor: Cursor) -> pd.DataFrame:
    """Function gets the latest plant health metrics including: temperature, soil moisture levels
    plant name, time of recording and last_watered, and extracts these to a dataframe."""

    query = f"""
        SELECT pm.temperature, pm.soil_moisture, latest_recording_info.latest_time,
          p.plant_name, pm.plant_id, pm.last_watered
        FROM {environ['SCHEMA_NAME']}.plant_metric pm
        JOIN (SELECT plant_id,
            MAX(recording_taken) as latest_time
            FROM {environ['SCHEMA_NAME']}.plant_metric
            GROUP BY plant_id) as latest_recording_info
        ON pm.plant_id = latest_recording_info.plant_id
            AND pm.recording_taken = latest_recording_info.latest_time
        JOIN {environ['SCHEMA_NAME']}.plant as p ON pm.plant_id = p.plant_id;
        """
    cursor.execute(query)
    result = cursor.fetchall()

    return pd.DataFrame(result)


def get_archival_data(cursor: Cursor) -> pd.DataFrame:
    """Function gets archival data including averages of temperature, soil_moisture."""

    query = f"""
        SELECT 
            ROUND(pa.avg_temperature, 2) AS avg_temperature, 
            ROUND(pa.avg_soil_moisture, 2) as avg_soil_moisture, 
            p.plant_name, 
            p.plant_id
        FROM {environ['SCHEMA_NAME']}.Plants_archive as pa
         JOIN (SELECT plant_id,
            MAX(last_recorded) as latest_time
            FROM {environ['SCHEMA_NAME']}.Plants_archive
            GROUP BY plant_id) as last_recording
        ON pa.plant_id = last_recording.plant_id
        JOIN {environ['SCHEMA_NAME']}.plant as p
            ON pa.plant_id = p.plant_id;
        """
    cursor.execute(query)
    result = cursor.fetchall()

    return pd.DataFrame(result)
