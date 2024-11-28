"""Test file for queries.py"""

import pytest
from unittest.mock import Mock


class TestingDBQueries:

    @pytest.fixture
    def mock_cursor(self):
        """Mock cursor to avoid real world db connections."""
        return Mock()


# tests to write
