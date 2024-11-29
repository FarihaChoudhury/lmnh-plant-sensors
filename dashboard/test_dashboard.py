"""Test file for queries.py"""
# pylint: skip-file
from os import environ
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from dashboard import (
    filter_by_plant, link_plant_name_id, get_data_plant_table)


class TestingDashboardFunctions:
    """Test Class for non-streamlit dashboard functions."""

    # @pytest.fixture
    # def sample_input_data(self):
    #     """Sample input data for tests."""
    #     return pd.DataFrame({
    #         'plant_id': [1, 2, 3],
    #         'plant_name': ['Fern', 'Cactus', 'Bamboo']
    #     })

    def test_filter_with_selected_plants(self):
        """Test filtering selected plants works as expected."""
        plant_metrics_input = pd.DataFrame({
            'plant_name': ['Fern', 'Cactus', 'Bamboo', 'Rose'],
            'metric_value': [10, 15, 20, 25]
        })
        archive_plants_input = pd.DataFrame({
            'plant_name': ['Fern', 'Cactus', 'Orchid'],
            'metric_value': [5, 7, 9]
        })
        selected_plants = ['Fern', 'Cactus']

        expected_plant_metrics = pd.DataFrame({
            'plant_name': ['Fern', 'Cactus'],
            'metric_value': [10, 15]
        })
        expected_archive_plants = pd.DataFrame({
            'plant_name': ['Fern', 'Cactus'],
            'metric_value': [5, 7]
        })

        result = filter_by_plant(
            selected_plants, plant_metrics_input, archive_plants_input)

        assert_frame_equal(result[0], expected_plant_metrics)
        assert_frame_equal(result[1], expected_archive_plants)

    def test_filter_without_selected_plants(self):
        """ Test no filtering returns all plants available"""
        plant_metrics = pd.DataFrame({
            'plant_name': ['Fern', 'Cactus', 'Bamboo', 'Rose'],
            'metric_value': [10, 15, 20, 25]
        })
        archive_plants = pd.DataFrame({
            'plant_name': ['Fern', 'Cactus', 'Orchid'],
            'metric_value': [5, 7, 9]
        })
        selected_plants = []

        result = filter_by_plant(
            selected_plants, plant_metrics, archive_plants)

        assert_frame_equal(result[0], plant_metrics)
        assert_frame_equal(result[1], archive_plants)

    def test_link_plant_name_id(self):
        """Test that the plant name and id can be linked together properly."""
        input_data = pd.DataFrame({
            'plant_id': [1, 2, 3],
            'plant_name': ['Fern', 'Cactus', 'Bamboo']
        })
        expected_data = pd.DataFrame({
            'plant_id': [1, 2, 3],
            'plant_name': ['Fern', 'Cactus', 'Bamboo'],
            'plant_id_name': [
                'Fern (ID: 1)',
                'Cactus (ID: 2)',
                'Bamboo (ID: 3)'
            ]
        })

        result = link_plant_name_id(input_data)
        assert_frame_equal(result, expected_data)

    def test_get_data_plant_table(self):
        """Test getting the plant data table works correctly."""
        input_data = {
            'plant_id': [102, 101, 103],
            'plant_name': ['Fern', 'Cactus', 'Bamboo']
        }

        expected_df = pd.DataFrame({
            'Plant Name': ['Cactus', 'Fern', 'Bamboo']
        }, index=pd.Index([101, 102, 103], name='Plant ID'))

        result_df = get_data_plant_table(input_data)
        assert_frame_equal(result_df, expected_df)
