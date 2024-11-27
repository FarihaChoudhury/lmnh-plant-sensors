"""Streamlit Dashboard for LNMH Plant Monitoring System."""

from os import environ
import logging
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
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


def homepage():
    """Homepage showing visualizations for LNMH."""
    st.title("LNMH Plant Monitoring System")


if __name__ == "__main__":
    load_dotenv()
    homepage()
