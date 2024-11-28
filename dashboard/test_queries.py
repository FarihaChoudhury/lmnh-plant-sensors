"""Test file for queries.py"""
# pylint: skip-file 
from os import environ
import pandas as pd
import pytest
import logging
from unittest.mock import Mock, MagicMock, patch
from pymssql import exceptions

from db_queries import (get_connection, get_cursor,
                        get_archival_data, get_latest_metrics)


class TestingDBQueries:
    """Test Class for db_queries file."""

    @pytest.fixture
    def mock_cursor(self):
        """Mock cursor to avoid real world db connections."""
        return Mock()
    @patch.dict(
        environ,
        {
            "DB_HOST": "mock_value",
            "DB_NAME": "mock_value",
            "DB_USER": "mock_value",
            "DB_PASSWORD": "mock_value",
            "DB_PORT": "mock_value",
            "SERVER": "mock_value"
        },
    )
    @patch('db_queries.connect')
    def test_get_connection_success(self, mock_connect):
        """Test successful database connection."""

        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        connection = get_connection()

        mock_connect.assert_called_once_with(
            server='mock_value',
            port='mock_value',
            user='mock_value',
            password='mock_value',
            database='mock_value',
            as_dict=True
        )
        assert connection == mock_connect.return_value

    @patch.dict(
        environ,
        {
            "DB_HOST": "mock_value",
            "DB_USER": "mock_value",
            "DB_PASSWORD": "mock_value",
            "DB_PORT": "mock_value",
            "SERVER": "mock_value"
        },
    )
    @patch('db_queries.connect')
    def test_get_connection_missing_env_var(self, mock_connect):
        """Test name key error when connecting to the database."""
        with pytest.raises(KeyError) as error:
            get_connection()

        mock_connect.assert_not_called()
        assert str(error.value) == "'DB_NAME'"

    @patch.dict(
        environ,
        {
            "DB_HOST": "mock_value",
            "DB_NAME": "mock_value",
            "DB_USER": "mock_value",
            "DB_PASSWORD": "mock_value",
            "DB_PORT": "mock_value",
        },
    )
    @patch('db_queries.connect')
    def test_get_connection_operational_error(self, mock_connect):
        """Test OperationalError when database connection fails."""
        mock_connect.side_effect = exceptions.OperationalError(
            "Operational error occurred")

        with pytest.raises(exceptions.OperationalError) as error:
            get_connection()

        mock_connect.assert_called_once_with(
            server='mock_value',
            port='mock_value',
            user='mock_value',
            password='mock_value',
            database='mock_value',
            as_dict=True
        )
        assert str(error.value) == "Operational error occurred"


    @patch("db_queries.connect")
    @patch("db_queries.environ", {"SCHEMA_NAME": "test_schema"})
    def test_successful_latest_metrics(self, mock_connect):
        """Test that latest temp and soil metrics retrieved successfully."""
    
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
                {
                    "temperature": 22.5,
                    "soil_moisture": 35.2,
                    "latest_time": "2024-11-27 14:30:00",
                    "plant_name": "Aloe Vera",
                    "plant_id": 1,
                    "last_watered": "2024-11-26 10:00:00"
                },
                {
                    "temperature": 24.1,
                    "soil_moisture": 40.5,
                    "latest_time": "2024-11-27 15:45:00",
                    "plant_name": "Snake Plant",
                    "plant_id": 2,
                    "last_watered": "2024-11-25 08:30:00"
                }
            ]

        result = get_latest_metrics(mock_cursor)

        assert result.shape == (2, 6)
        assert isinstance(result, pd.DataFrame)
        assert set(result.columns) == {"temperature", 
                                       "soil_moisture", "latest_time", 
                                       "plant_name", "plant_id", "last_watered"}
    
    @patch("db_queries.connect")
    @patch("db_queries.environ", {"SCHEMA_NAME": "test_schema"})
    def test_unsuccessful_latest_metrics(self, mock_connect, caplog):
        """Test that unsuccessful retrieval is handled gracefully. """

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = None


        
        with caplog.at_level(logging.WARNING):
            get_latest_metrics(mock_cursor)

        assert "No data to insert into the plant_metric table." in caplog.text
        mock_connection.cursor.assert_not_called()


# tests to write
# test valid connection
# test bad connection
# test cursor good
# test latest_metrics
# test archival
# test empty results handling


