import os

import unittest
from unittest.mock import MagicMock, patch, call
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
        with self.assertRaises(KeyError):
            get_connection()

    @patch("archive.connect")
    def test_get_connection_operational_error(self, mock_connect):
        mock_connect.side_effect = Exception("OperationalError")
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

        mock_cursor.execute.assert_called_once_with(
            "TRUNCATE TABLE epsiplant_metric;")

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


if __name__ == "__main__":
    unittest.main()
