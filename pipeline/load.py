from os import environ
import logging
from dotenv import load_dotenv
import pandas as pd
from pymssql import connect, Connection, exceptions


def get_connection() -> connect:
    """Connects to Microsoft SQL Server Database"""
    logging.info("Connected to database")
    try:
        return connect(
            server=environ["DB_HOST"],
            port=environ["DB_PORT"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
            database=environ["DB_NAME"],
            as_dict=True
        )
    except KeyError as e:
        logging.error("%s missing from environment variables.", e)
    except exceptions.OperationalError as e:
        logging.error("Error connecting to database: %s", e)


def get_table_id(connection: Connection, table_name: str, name: str) -> int:
    """Gets the id of a botanist or plant by a given plant name"""

    if table_name == "epsilon.botanist":
        table_col = "botanist_id"
        query = f"""SELECT botanist_id from epsilon.botanist WHERE full_name LIKE '%{
            name}%'"""
    elif table_name == "epsilon.plant":
        table_col = "plant_id"
        query = f"""SELECT plant_id from epsilon.plant WHERE plant_name LIKE '%{
            name}%'"""
    with connection.cursor() as cur:
        print(f"Query is :{query}")
        cur.execute(query,)
        id = cur.fetchone()[table_col]
        print(id)

    return id


def get_plant_metric_data() -> pd.DataFrame:
    return pd.read_csv("./clean_plant_info.csv")


def insert_into_plant_metric(connection: Connection, metric_df: pd.DataFrame) -> None:
    """Inserts data into the table plant_metric"""

    for _, row in metric_df.iterrows():

        logging.info(f"Adding to db: {row['plant_name']}")
        print("row", _)

        botanist_id = get_table_id(connection, "epsilon.botanist", row['name'])
        plant_id = get_table_id(
            connection, "epsilon.plant", row['plant_name'].replace(",", "").replace("'", ""))

        query = """INSERT INTO epsilon.plant_metric (temperature, soil_moisture,
        recording_taken, last_watered, botanist_id, plant_id) VALUES
        (%s, %s, %s, %s, %s, %s)"""

        with connection.cursor() as cur:
            print(botanist_id)
            print(plant_id)
            print("")
            cur.execute(query, (row['temperature'], row['soil_moisture'],
                                row['recording_taken'], row['last_watered'], botanist_id, plant_id))
        logging.info("Query successfully executed")
        connection.commit()
    connection.close()
    logging.info("Connection closed")


def main():
    load_dotenv()
    metric_df = get_plant_metric_data()
    conn = get_connection()
    insert_into_plant_metric(conn, metric_df)


if __name__ == "__main__":
    main()
