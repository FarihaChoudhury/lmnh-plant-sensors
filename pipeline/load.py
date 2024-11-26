from os import environ
import logging
from dotenv import load_dotenv
import pandas as pd
from pymssql import connect, Connection, exceptions


def get_connection():
    """Connects to Microsoft SQL Server Database"""
    logging.info("Connected to database")
    return connect(
        server=environ["DB_HOST"],
        port=environ["DB_PORT"],
        user=environ["DB_USER"],
        password=environ["DB_PASSWORD"],
        database=environ["DB_NAME"],
        as_dict=True
    )


def get_id():
    """Gets the id of a botanist or plant"""


def main():
    ...


if __name__ == "__main__":
    main()
