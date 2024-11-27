"""Uploads data from a CSV file into a database"""

from os import environ
import logging
from dotenv import load_dotenv
import pandas as pd
from pymssql import connect, Connection, exceptions

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


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


def get_botanists_id_mapping(connection: Connection, names: list) -> dict:
    """Fetches botanist IDs for a list of names."""
    logging.info("Fetching botanist IDs for names: %s", names)
    query = f"""SELECT botanist_id, full_name FROM epsilon.botanist WHERE full_name IN ({
        ', '.join(['%s'] * len(names))})"""
    try:
        with connection.cursor() as cur:
            cur.execute(query, names)
            result = cur.fetchall()
            if not result:
                logging.warning("No botanists found for the provided names.")
            return {botanist['full_name']: botanist['botanist_id'] for botanist in result}
    except exceptions.DatabaseError as e:
        logging.error("Database error while fetching botanist IDs: %s", e)
        raise
    except Exception as e:
        logging.error("Unexpected error while fetching botanist IDs: %s", e)
        raise


def insert_into_plant_metric(connection: Connection, metric_df: pd.DataFrame, botanist_id_mapping: dict) -> None:
    """Inserts plant metric data into the database."""
    query = """INSERT INTO epsilon.plant_metric (temperature, soil_moisture,
                recording_taken, last_watered, botanist_id, plant_id) 
                VALUES (%s, %s, %s, %s, %s, %s)"""

    data_to_insert = metric_df.apply(
        lambda row: (
            row['temperature'],
            row['soil_moisture'],
            row['recording_taken'],
            row['last_watered'],
            botanist_id_mapping.get(row['name']),
            row['plant_id']
        ), axis=1).tolist()

    if data_to_insert:
        try:
            with connection.cursor() as cur:
                cur.executemany(query, data_to_insert)
                connection.commit()
                logging.info(
                    f"Inserted {len(data_to_insert)} rows into the plant_metric table.")
        except exceptions.DatabaseError as e:
            logging.error(
                "Database error while inserting plant metric data: %s", e)
            raise
        except Exception as e:
            logging.error(
                "Unexpected error while inserting plant metric data: %s", e)
            raise
    else:
        logging.warning("No data to insert into the plant_metric table.")


def main(plant_metrics_df: pd.DataFrame):
    """ Loads the plant readings into the MS-SQL RDS database. """
    load_dotenv()

    try:

        with get_connection() as conn:
            botanist_names = plant_metrics_df['name'].unique().tolist()

            botanist_id_mapping = get_botanists_id_mapping(
                conn, botanist_names)

            insert_into_plant_metric(
                conn, plant_metrics_df, botanist_id_mapping)
    except exceptions.OperationalError as e:
        logging.error("Failed to connect to the database: %s", e)
        raise
    except Exception as e:
        logging.error(
            "An error occurred during the execution of the program: %s", e)


if __name__ == "__main__":
    main()
