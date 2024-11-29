"""Test file for the db_queries.py which queries the database for dashboard"""
# pylint: skip-file
from os import environ
import pandas as pd
import pytest
import logging
from unittest.mock import Mock, MagicMock, patch
from pymssql import exceptions

from db_queries import (get_connection, get_cursor,
                        get_archival_data, get_latest_metrics, get_plant_image_url,
                        get_plant_countries, get_plant_fact)


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

    @patch.dict(
        environ,
        {
            "DB_HOST": "mock_value",
            "DB_NAME": "mock_value",
            "DB_USER": "mock_value",
            "DB_PASSWORD": "mock_value",
            "DB_PORT": "mock_value",
        },)
    @patch('db_queries.connect')
    def test_get_connection_exception(self, mock_connect):
        """Test General Exception when database connection fails."""
        mock_connect.side_effect = Exception(
            "Unexpected error while connecting to database:")

        with pytest.raises(Exception) as error:
            get_connection()

        mock_connect.assert_called_once_with(
            server='mock_value',
            port='mock_value',
            user='mock_value',
            password='mock_value',
            database='mock_value',
            as_dict=True
        )
        assert str(
            error.value) == "Unexpected error while connecting to database:"

    @patch.dict(
        environ,
        {
            "DB_HOST": "mock_value",
            "DB_NAME": "mock_value",
            "DB_USER": "mock_value",
            "DB_PASSWORD": "mock_value",
            "DB_PORT": "mock_value",
        },)
    @patch('db_queries.connect')
    def test_get_cursor(self, mock_connect):
        """Test the get_cursor function returns a valid cursor."""

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        cursor = get_cursor(mock_connection)

        mock_connection.cursor.assert_called_once()
        assert cursor == mock_cursor

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
    def test_unsuccessful_latest_metrics_operational(self, mock_connect, caplog):
        """Test that unsuccessful retrieval is handled gracefully with Operational Error. """

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.execute.side_effect = exceptions.OperationalError(
            "Simulated database error")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(exceptions.OperationalError):
                get_latest_metrics(mock_cursor)

            assert "Operational error occurred connecting whilst fetching live metrics" in caplog.text
            mock_cursor.execute.assert_called_once()
            mock_cursor.fetchall.assert_not_called()

    @patch("db_queries.connect")
    @patch("db_queries.environ", {"SCHEMA_NAME": "test_schema"})
    def test_unsuccessful_latest_metrics_exception(self, mock_connect, caplog):
        """Test that unsuccessful retrieval is handled gracefully with fallback general exception. """

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.execute.side_effect = Exception("Simulated database error")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(Exception):
                get_latest_metrics(mock_cursor)

            assert "Error occurred whilst fetching live metrics:" in caplog.text
            mock_cursor.execute.assert_called_once()
            mock_cursor.fetchall.assert_not_called()

    @patch("db_queries.connect")
    @patch("db_queries.environ", {"SCHEMA_NAME": "test_schema"})
    def test_successful_archival_metrics(self, mock_connect):
        """Test that archival temp and soil metrics retrieved successfully."""

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            {"avg_temperature": 22.5, "avg_soil_moisture": 30.4,
                "plant_name": "Aloe Vera", "plant_id": 1},
            {"avg_temperature": 25.0, "avg_soil_moisture": 50.0,
                "plant_name": "Bamboo", "plant_id": 2},
        ]

        result = get_archival_data(mock_cursor)

        assert result.shape == (2, 4)
        assert isinstance(result, pd.DataFrame)
        assert set(result.columns) == {
            'plant_id', 'avg_soil_moisture', 'plant_name', 'avg_temperature'}

    @patch("db_queries.connect")
    @patch("db_queries.environ", {"SCHEMA_NAME": "test_schema"})
    def test_unsuccessful_archival_metrics_operational(self, mock_connect, caplog):
        """Test that unsuccessful retrieval is handled gracefully with operational error. """

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.execute.side_effect = exceptions.OperationalError(
            "Simulated database error")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(exceptions.OperationalError):
                get_latest_metrics(mock_cursor)

            assert "Operational error occurred connecting whilst fetching live metrics" in caplog.text
            mock_cursor.execute.assert_called_once()
            mock_cursor.fetchall.assert_not_called()

    @patch("db_queries.connect")
    @patch("db_queries.environ", {"SCHEMA_NAME": "test_schema"})
    def test_unsuccessful_archival_exception(self, mock_connect, caplog):
        """Test that unsuccessful retrieval is handled gracefully with fallback general error. """

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.execute.side_effect = Exception("Simulated database error")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(Exception):
                get_archival_data(mock_cursor)

            assert "Error occurred whilst fetching archival metrics:" in caplog.text
            mock_cursor.execute.assert_called_once()
            mock_cursor.fetchall.assert_not_called()

    @patch("db_queries.connect")
    @patch("db_queries.environ", {"SCHEMA_NAME": "test_schema"})
    def test_successful_link(self, mock_connect):
        """Test that archival temp and soil metrics retrieved successfully."""

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = pd.DataFrame(
            [{'image_url': 'test.com'}])

        result = get_plant_image_url(mock_cursor, 'test')
        assert isinstance(result, pd.DataFrame)
        assert set(result.columns) == {'image_url'}

    @patch("db_queries.connect")
    @patch("db_queries.environ", {"SCHEMA_NAME": "test_schema"})
    def test_unsuccessful_plant_url_operational(self, mock_connect, caplog):
        """Test that unsuccessful retrieval is handled gracefully with operational error. """

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.execute.side_effect = exceptions.OperationalError(
            "Simulated database error")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(exceptions.OperationalError):
                get_plant_image_url(mock_cursor, 'test')

            assert "Operational error occurred connecting whilst fetching live metrics" in caplog.text
            mock_cursor.execute.assert_called_once()
            mock_cursor.fetchall.assert_not_called()

    @patch("db_queries.connect")
    @patch("db_queries.environ", {"SCHEMA_NAME": "test_schema"})
    def test_unsuccessful_plant_url_exception(self, mock_connect, caplog):
        """Test that unsuccessful retrieval is handled gracefully with fallback general exception. """

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.execute.side_effect = Exception("Simulated database error")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(Exception):
                get_plant_image_url(mock_cursor, 'test')

            assert "Error occurred whilst fetching plant image url" in caplog.text
            mock_cursor.execute.assert_called_once()
            mock_cursor.fetchall.assert_not_called()


class TestingGenAIResponses:
    """"Test Class for the functions that interact with GenAI."""

    def test_get_plant_fact_successful(self):
        """Test that the plant fact retrieval is successful."""

        mock_model = MagicMock()
        fake_return_value = {
            'candidates': [
                {'content': {
                    'parts': [{'text': 'Sunflowers can grow up to 12 feet tall!'}]}}
            ]
        }
        mock_model.generate_content.return_value.to_dict.return_value = fake_return_value
        plant_name = "sunflower"
        plant_fact = 'Sunflowers can grow up to 12 feet tall!'
        response = get_plant_fact(mock_model, plant_name)

        assert response == plant_fact

    def test_get_plant_countries_successful(self):
        """Test that the plant countries retrieval is successful."""

        mock_model = MagicMock()
        fake_return_value = {
            'candidates': [
                {'content': {
                    'parts': [{'text': 'Sunflowers are native to North and Central America.'}]}}
            ]
        }
        mock_model.generate_content.return_value.to_dict.return_value = fake_return_value
        plant_name = "sunflower"
        plant_fact = 'Sunflowers are native to North and Central America.'
        response = get_plant_countries(mock_model, plant_name)

        assert response == plant_fact
