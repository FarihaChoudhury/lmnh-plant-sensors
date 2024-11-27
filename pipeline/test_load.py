import os
import pytest
from unittest.mock import patch, MagicMock

from load import get_connection, get_botanists_id_mapping


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
def test_get_connection_success(mock_connect):
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


@patch('load.connect')
def test_get_botanists_id_mapping_successful(mock_connect):
    mock_connection = MagicMock()

    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'botanist_id': 1, 'full_name': 'Alice'},
        {'botanist_id': 2, 'full_name': 'Bob'}
    ]
    result = get_botanists_id_mapping(mock_connection, ['Alice', 'Bob'])

    assert result == {'Alice': 1, 'Bob': 2}


# def test_get_plant_metric_data_successful():
#
