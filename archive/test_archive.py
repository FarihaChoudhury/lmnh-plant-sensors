from archive import (get_connection, get_all_plant_ids,
                     get_plants_data, upload_plant_metric_data, calculate_archive_metrics, get_latest_recording, clear_plant_metrics)


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


class TestPlantETL(unittest.TestCase):

    @patch("archive.connect")
    @patch("archive.environ")
    def test_get_connection_success(self, mock_environ, mock_connect):
        mock_environ.__getitem__.side_effect = lambda key: {
            "DB_HOST": "localhost",
            "DB_PORT": "1433",
            "DB_USER": "user",
            "DB_PASSWORD": "password",
            "DB_NAME": "database"
        }[key]

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn = get_connection()
        self.assertEqual(conn, mock_conn)
        mock_connect.assert_called_once()

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
