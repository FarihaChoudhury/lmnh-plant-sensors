"""db_queries.py: data retrieval for dashboard visualisations."""
# pylint: disable=no-name-in-module

from os import environ
import logging
import pandas as pd
from pymssql import connect, Connection, exceptions, Cursor


def get_connection() -> Connection:
    """Connects to Microsoft SQL Server Database"""

    logging.info("Attempting to connect to the database.")
    try:
        conn = connect(
            server=environ["DB_HOST"],
            port=environ["DB_PORT"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
            as_dict=True
        )
        logging.info("Database connection successful.")
        return conn
    except KeyError as e:
        logging.error("%s missing from environment variables.", e)
        raise
    except exceptions.OperationalError as e:
        logging.error("Error connecting to database: %s", e)
        raise
    except Exception as e:
        logging.error("Unexpected error while connecting to database: %s", e)
        raise


def get_cursor(connection: Connection) -> Cursor:
    """Cursor to execute commands in db"""
    return connection.cursor()


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
    try:

        cursor.execute(query)
        result = cursor.fetchall()
    except exceptions.OperationalError as e:
        logging.error(
            "Operational error occurred connecting whilst fetching live metrics: %s", e)
        raise
    except Exception as e:
        logging.error("Error occurred whilst fetching live metrics: %s", e)
        raise

    return pd.DataFrame(result)


def get_archival_data(cursor: Cursor) -> pd.DataFrame:
    """Function gets archival data including averages of temperature, soil_moisture."""

    query = f"""
        SELECT ROUND(AVG(pa.avg_temperature), 2) AS avg_temperature,
        ROUND(AVG(pa.avg_soil_moisture), 2) AS avg_soil_moisture,
        p.plant_name, p.plant_id
        FROM epsilon.plants_archive AS pa
        JOIN epsilon.plant AS p
        ON p.plant_id = pa.plant_id
        GROUP BY p.plant_name, p.plant_id;
        """
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except exceptions.OperationalError as e:
        logging.error(
            "Operational error occurred connecting whilst fetching live metrics: %s", e)
        raise
    except Exception as e:
        logging.error("Error occurred whilst fetching archival metrics: %s", e)
        raise

    return pd.DataFrame(result)


def get_plant_image_url(cursor: Cursor, plant_name: str) -> str:
    """Extracts the plant image url for a plant by its name."""
    query = """ SELECT image_url
                FROM epsilon.plant 
                WHERE plant_name = %s;"""

    try:
        cursor.execute(query, (plant_name,))
        result = cursor.fetchone()
    except exceptions.OperationalError as e:
        logging.error(
            "Operational error occurred connecting whilst fetching live metrics: %s", e)
        raise
    except Exception as e:
        logging.error("Error occurred whilst fetching plant image url: %s", e)
        raise
    return result
