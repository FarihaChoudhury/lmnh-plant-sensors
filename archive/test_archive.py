""" Test file for archive plant data"""
# pylint: skip-file

import os
import unittest
from unittest.mock import MagicMock, patch, call
from pymssql import exceptions
from archive import (
    get_connection,
    get_all_plant_ids,
    get_plants_data,
    upload_plant_metric_data,
    calculate_archive_metrics,
    get_latest_recording,
    clear_plant_metrics,
    lambda_handler
)


class TestArchive(unittest.TestCase):
    """ Test class containing archive tests """
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
    @patch('archive.connect')
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

    @patch("archive.connect")
    def test_get_connection_missing_env_var(self, mock_connect):
        """"""
        with self.assertRaises(KeyError):
            get_connection()

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
    @patch("archive.connect")
    def test_get_connection_operational_error(self, mock_connect):
        """"""
        mock_connect.side_effect = exceptions.OperationalError(
            "OperationalError")

        with self.assertRaises(exceptions.OperationalError):
            get_connection()

    @patch("archive.connect")
    def test_get_connection_unexpected_error(self, mock_connect):
        """"""
        mock_connect.side_effect = Exception("UnexpectedError")
        with self.assertRaises(Exception):
            get_connection()

    @patch("archive.get_connection")
    def test_get_all_plant_ids(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"plant_id": 1}, {"plant_id": 2}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        plant_ids = get_all_plant_ids(mock_conn)
        self.assertEqual(plant_ids, [1, 2])
        mock_cursor.execute.assert_called_once_with(
            "SELECT plant_id FROM plant;")

    @patch("archive.upload_plant_metric_data")
    @patch("archive.get_latest_recording")
    @patch("archive.calculate_archive_metrics")
    def test_get_plants_data(self, mock_calculate_metrics, mock_get_latest_recording, mock_upload_data):
        mock_conn = MagicMock()
        plant_ids = [1, 2]

        mock_calculate_metrics.side_effect = [
            [{"avg_moisture": 0.5, "watered_count": 2, "avg_temp": 25}],
            [{"avg_moisture": 0.6, "watered_count": 3, "avg_temp": 22}]
        ]

        mock_get_latest_recording.side_effect = [
            {"recording_taken": "2024-11-27 10:00:00"},
            {"recording_taken": "2024-11-27 11:00:00"}
        ]

        get_plants_data(mock_conn, plant_ids)

        mock_upload_data.assert_has_calls([
            call(mock_conn, {
                "avg_moisture": 0.5,
                "watered_count": 2,
                "avg_temp": 25,
                "last_recorded": "2024-11-27 10:00:00",
                "plant_id": 1
            }),
            call(mock_conn, {
                "avg_moisture": 0.6,
                "watered_count": 3,
                "avg_temp": 22,
                "last_recorded": "2024-11-27 11:00:00",
                "plant_id": 2
            })
        ])

    @patch("archive.get_connection")
    def test_clear_plant_metrics(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        clear_plant_metrics(mock_conn)

        expected_query = "TRUNCATE TABLE epsilon.plant_metric;"

        mock_cursor.execute.assert_called_once_with(expected_query)

    @patch("archive.get_connection")
    @patch("archive.get_all_plant_ids")
    @patch("archive.get_plants_data")
    @patch("archive.clear_plant_metrics")
    def test_lambda_handler_success(self, mock_clear, mock_get_data, mock_get_ids, mock_get_conn):
        mock_get_conn.return_value = MagicMock()
        mock_get_ids.return_value = [1, 2]

        response = lambda_handler(None, None)
        self.assertEqual(response["statuscode"], 200)
        mock_get_ids.assert_called_once()
        mock_get_data.assert_called_once()
        mock_clear.assert_called_once()

    @patch("archive.get_connection")
    def test_lambda_handler_failure(self, mock_get_conn):
        mock_get_conn.side_effect = Exception("Connection Error")
        response = lambda_handler(None, None)
        self.assertEqual(response["statusCode"], 500)
        self.assertIn("An unexpected error occurred", response["body"])

    @patch("archive.get_connection")
    def test_upload_plant_metric_data_valid(self, mock_get_conn):
        """Test successful execution with valid plant details."""
        mock_get_conn.return_value = MagicMock()
        mock_cursor = mock_get_conn.cursor.return_value.__enter__.return_value

        plant_details = {
            "avg_temp": 25.3,
            "avg_moisture": 70.5,
            "watered_count": 3,
            "last_recorded": "2024-11-27 15:00:00",
            "plant_id": 101
        }

        upload_plant_metric_data(mock_get_conn, plant_details)

        mock_cursor.execute.assert_called_once_with(
            """INSERT INTO epsilon.plants_archive (avg_temperature, 
                    avg_soil_moisture, watered_count, last_recorded, plant_id)
                VALUES (%s, %s, %s, %s, %s);""", (25.3, 70.5, 3, "2024-11-27 15:00:00", 101))

    @ patch("archive.get_connection")
    def test_calculate_archive_metrics(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"avg_moisture": 1}, {"watered_count": 2}, {"avg_temp": 2}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        expected_query = """SELECT
                    AVG(soil_moisture) as avg_moisture,
                    COUNT(DISTINCT(last_watered)) as watered_count,
                    AVG(temperature) as avg_temp
                FROM plant_metric
                WHERE plant_id = %s"""

        calculate_archive_metrics(mock_conn, 1)
        mock_cursor.execute.assert_called_once_with(expected_query, (1,))

    @ patch("archive.get_connection")
    def test_get_latest_recording(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"recording_taken": "1"}]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        expected_query = """SELECT TOP 1 recording_taken
                FROM plant_metric
                WHERE plant_id = %s
                ORDER BY recording_taken DESC;"""

        get_latest_recording(mock_conn, 1)
        mock_cursor.execute.assert_called_once_with(expected_query, (1,))
