"""Test file for loading plant data to database"""
# pylint: skip-file

import os
import pytest
import pandas as pd
import logging
from unittest.mock import patch, MagicMock
from pymssql import exceptions

from load import get_connection, get_botanists_details, insert_plant_metric, main


class TestLoadPlantData():
    """ Test class containing load tests """

    @pytest.fixture
    def mock_df(self):
        return pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'temperature': [22, 24],
            'soil_moisture': [50, 55],
            'recording_taken': ['2024-11-27', '2024-11-27'],
            'last_watered': ['2024-11-25', '2024-11-26'],
            'plant_id': [1, 2]
        })

    @pytest.fixture
    def mock_df_2(self):
        return pd.DataFrame({
            'name': ['Alice'],
            'temperature': [22],
            'soil_moisture': [50],
            'recording_taken': ['2024-11-27'],
            'last_watered': ['2024-11-25'],
            'plant_id': [1]
        })

    @patch.dict(
        os.environ,
        {
            "DB_HOST": "mock_value",
            "DB_NAME": "mock_value",
            "DB_USER": "mock_value",
            "DB_PASSWORD": "mock_value",
            "DB_PORT": "mock_value",
            "SERVER": "mock_value"
        },
    )
    @patch('load.connect')
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
        os.environ,
        {
            "DB_HOST": "mock_value",
            "DB_NAME": "mock_value",
            "DB_USER": "mock_value",
            "DB_PASSWORD": "mock_value",
            "DB_PORT": "mock_value",
        },
    )
    @patch('load.connect')
    def test_get_connection_operational_error(self, mock_connect):
        """Test OperationalError when database connection fails."""
        mock_connect.side_effect = exceptions.OperationalError(
            "Operational error occurred")

        with pytest.raises(exceptions.OperationalError) as error:
            get_connection()

    @patch('load.connect')
    def test_get_botanists_id_mapping_successful(self, mock_connect):
        """Tests if the botanists details are successfully retrieved."""
        mock_connection = MagicMock()

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'botanist_id': 1, 'full_name': 'Alice'},
            {'botanist_id': 2, 'full_name': 'Bob'}
        ]
        result = get_botanists_details(mock_connection, ['Alice', 'Bob'])

        assert result == {'Alice': 1, 'Bob': 2}

    @patch('load.connect')
    def test_get_botanists_id_mapping_unsuccessful(self, mock_connect):
        """Tests to see if None is returned for invalid botanist names"""
        mock_connection = MagicMock()

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = None
        result = get_botanists_details(mock_connection, ['', ''])

        assert result == None

    @patch('load.Connection')
    def test_get_botanists_details_database_error(self, mock_connection):
        """Test DatabaseError during botanist details retrieval."""
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.execute.side_effect = exceptions.DatabaseError(
            "Simulated database error")
        names = ["Alice", "Bob"]

        with pytest.raises(exceptions.DatabaseError) as error:
            get_botanists_details(mock_connection, names)

    @patch('load.connect')
    def test_insert_plant_metric_successful(self, mock_connect, mock_df):
        """Tests whether the plant metric data is successfully inserted via mocking"""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_connection

        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        botanist_details = {'Alice': 1, 'Bob': 2}

        insert_plant_metric(mock_connection, mock_df, botanist_details)

        expected_data = [
            (22, 50, '2024-11-27', '2024-11-25', 1, 1),
            (24, 55, '2024-11-27', '2024-11-26', 2, 2)
        ]

        mock_cursor.executemany.assert_called_once_with(
            """INSERT INTO epsilon.plant_metric (temperature, soil_moisture,
                recording_taken, last_watered, botanist_id, plant_id) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
            expected_data
        )
        mock_connection.commit.assert_called_once()

    @patch('load.connect')
    def test_insert_plant_metric_empty_df(self, mock_connect, caplog):
        """Tests to see if the correct logging is raised if there is no data to insert."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value = mock_connection

        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        metric_df = pd.DataFrame(columns=[
            'temperature', 'soil_moisture', 'recording_taken', 'last_watered', 'name', 'plant_id'
        ])
        botanist_details = {'Alice': 1}

        with caplog.at_level(logging.WARNING):
            insert_plant_metric(mock_connection, metric_df, botanist_details)

        assert "No data to insert into the plant_metric table." in caplog.text
        mock_connection.cursor.assert_not_called()

    @patch('load.connect')
    def test_insert_plant_metric_database_error(self, mock_connection, mock_df_2):
        """Test DatabaseError during plant metric insertion."""
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.executemany.side_effect = exceptions.DatabaseError(
            "Simulated database error")
        botanist_details = {'Alice': 1}

        with pytest.raises(exceptions.DatabaseError) as error:
            insert_plant_metric(mock_connection, mock_df_2, botanist_details)

    @patch('load.connect')
    def test_insert_plant_unexpected_error(self, mock_connection, mock_df_2):
        """Test unexpected exception during execution."""

        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.executemany.side_effect = Exception(
            "Unexpected error occurred")
        botanist_details = {'Alice': 1}

        with pytest.raises(Exception) as error:
            insert_plant_metric(mock_connection, mock_df_2, botanist_details)

    @patch('load.get_botanists_details')
    @patch('load.insert_plant_metric')
    @patch('load.get_connection')
    @patch('load.load_dotenv')
    def test_main_success(self, mock_load_dotenv, mock_get_connection, mock_insert_plant_metric, mock_get_botanists_details, mock_df):
        """Test successful execution of the main function."""
        mock_connection = MagicMock()
        mock_get_connection.return_value.__enter__.return_value = mock_connection

        mock_get_botanists_details.return_value = {"Alice": 1, "Bob": 2}

        main(mock_df)

        mock_load_dotenv.assert_called_once()
        mock_get_connection.assert_called_once()
        mock_get_botanists_details.assert_called_once_with(
            mock_connection, ["Alice", "Bob"])
        mock_insert_plant_metric.assert_called_once_with(
            mock_connection, mock_df, {"Alice": 1, "Bob": 2})

    @patch('load.get_connection')
    @patch('load.load_dotenv')
    def test_main_connection_error(self, mock_load_dotenv, mock_get_connection, mock_df):
        """Test OperationalError during database connection."""

        mock_get_connection.side_effect = exceptions.OperationalError(
            "Connection failed")

        with pytest.raises(exceptions.OperationalError) as error:
            main(mock_df)

    @patch('load.get_connection')
    @patch('load.load_dotenv')
    def test_main_unexpected_error(self, mock_load_dotenv, mock_get_connection, mock_df):
        """Test unexpected exception during execution."""

        mock_get_connection.side_effect = Exception(
            "Unexpected error occurred")

        with pytest.raises(Exception) as error:
            main(mock_df)
