"""
info needed from past 24 hours - average temp, avg soil, water count, last recording for each plant
"""
from pipeline import load
from pymssql import Connection


def upload_plant_metric_data(conn: Connection):
    """Uploads the past 24 hour data from plant metrics table into archive table"""
    query = """INSERT INTO plant_archive (plant_archive_id, avg_temperature, 
                avg_soil_moisture, watered_count, last_recorded, plant_id)
                SELECT * FROM plant_metrics;"""
    with conn.cursor() as cur:
        cur.execute(query)


def calculate_plant_water_count(conn: Connection, plant_id: int) -> int:
    """Calculates the number of times a given plant was watered in the last 24 hours"""
    # needs to count unique timestamps
    query = """SELECT COUNT(DISTINCT(last_watered)) as watered_count
                FROM plant_metric
                WHERE plant_id = %s"""
    with conn.cursor() as cur:
        cur.execute(query, (plant_id,))


def calculate_avg_soil_moisture(conn: Connection, plant_id: int) -> int:
    """Calculates the average soil moisture level for a given plant in the last 24 hours"""
    ...


def calculate_avg_temperature(conn: Connection, plant_id: int) -> int:
    """Calculates the average temperature for a given plant in the last 24 hours"""
    ...


def clear_plant_metrics(conn: Connection) -> None:
    """ Clears all recordings from the plant metrics table. """
    query = "TRUNCATE TABLE plant_metric;"
    with conn.cursor() as cur:
        cur.execute(query)


def main() -> None:
    """"""
    conn = load.get_connection()


def lambda_handler(event, context):
    """Moves data in the archive table and cleans the plant_metric table
    when the lambda is invoked"""
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


if __name__ == "__main__":
    ...
