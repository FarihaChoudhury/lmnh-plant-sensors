"""Test file for queries.py"""

from os import environ
import pytest
from unittest.mock import Mock, MagicMock, patch
from pymssql import exceptions

from db_queries import (get_connection, get_cursor,
                        get_archival_data, get_latest_metrics)


class TestingDBQueries:

    @pytest.fixture
    def mock_cursor(self):
        """Mock cursor to avoid real world db connections."""
        return Mock()

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
        environ,
        {
            "DB_HOST": "mock_value",
            "DB_USER": "mock_value",
            "DB_PASSWORD": "mock_value",
            "DB_PORT": "mock_value",
            "SERVER": "mock_value"
        },
    )
    @patch('load.connect')
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
    @patch('load.connect')
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

# tests to write
# test valid connection
# test bad connection
# test cursor good
# test latest_metrics
# test archival
# test empty results handling
