"""Test file for extracting plant data"""
# pylint: skip-file

import pytest
from unittest.mock import patch, mock_open, AsyncMock
import aiohttp
import asyncio

from extract import (extract_botanist_information,
                     extract_location_information,
                     extract_metric_information,
                     extract_plant_information,
                     fetch_plant_data,
                     collect_all_plant_data)


class TestExtractPlantInformation():
    """ Test class containing extract tests """

    @pytest.fixture
    def sample_api_information(self):
        return {
            "botanist": {
                "email": "test@test.com",
                "name": "Test Test",
                "phone": "+0000 111222"
            },
            "images": {
                "original_url": "https://test.jpg",
            },
            "last_watered": "Test time 1",
            "name": "Test Test",
            "origin_location": [
                "0",
                "1",
                "London",
                "GB",
            ],
            "plant_id": 11,
            "recording_taken": "Test time 2",
            "scientific_name": [
                "Test Test"
            ],
            "soil_moisture": 0,
            "temperature": 1
        }

    @pytest.mark.asyncio
    async def test_extract_botanist_information(self):
        """Tests extracts botanists information successfully """
        input_data = {"name": "Test Test",
                      "email": "test@test.com", "phone": "+0000 111222"}
        output_data = {"name": "Test Test",
                       "email": "test@test.com", "phone": "+0000 111222"}
        result = await extract_botanist_information(input_data)
        assert result == output_data

    @pytest.mark.asyncio
    async def test_extract_botanist_information_with_no_name(self):
        """Tests extracts botanist information without a name """
        input_data = {"name": None,
                      "email": "test@test.com", "phone": "+0000 111222"}
        output_data = {"name": None,
                       "email": "test@test.com", "phone": "+0000 111222"}
        result = await extract_botanist_information(input_data)
        assert result == output_data

    @pytest.mark.asyncio
    async def test_extract_location_information(self):
        """ Tests extracts correct location information and formats correctly"""
        input_data = ["1", "0", "London", "GB"]
        output_data = {"latitude": "0", "longitude": "1",
                       "closest_town": "London", "ISO_code": "GB"}
        result = await extract_location_information(input_data)
        assert result == output_data
        assert isinstance(output_data, dict)

    @pytest.mark.asyncio
    async def test_extract_metric_information(self):
        """ Tests extracts needed plant metrics information correctly """
        input_data = {"temperature": 0,
                      "soil_moisture": 0,
                      "recording_taken": "Test time 2",
                      "last_watered": "Test time 1",
                      "blah": "Test blah"}
        output_data = {"temperature": 0,
                       "soil_moisture": 0,
                       "recording_taken": "Test time 2",
                       "last_watered": "Test time 1"}
        result = await extract_metric_information(input_data)
        assert result == output_data

    @pytest.mark.asyncio
    async def test_extract_plant_information(self):
        """" Tests extracts plant metrics information correctly """
        input_data = {"plant_id": 1, "name": "Test Test",
                      "scientific_name": ["Test Test"]}
        output_data = {'image_url': 'None', "plant_id": 1, "name": "Test Test",
                       "scientific_name": "Test Test"}
        result = await extract_plant_information(input_data)
        print(result)
        assert result == output_data

    @pytest.mark.asyncio
    async def test_extract_plant_information_no_scientific_name(self):
        """" Tests extracts plant metrics information and sets scientific name
            to None if none were given. """
        input_data = {"plant_id": 1, "name": "Test Test"}
        output_data = {'image_url': 'None', "plant_id": 1, "name": "Test Test",
                       "scientific_name": "None"}
        result = await extract_plant_information(input_data)
        assert result == output_data

    @pytest.mark.asyncio
    @patch("extract.aiohttp.ClientSession.get")
    async def test_collect_all_plant_data(self, mock_get, sample_api_information):
        """ Test that fetching data contains name, plant_name and temperature """
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = sample_api_information

        mock_get.return_value = mock_response
        result = await collect_all_plant_data()

        for entry in result:
            assert "name" in entry
            assert "plant_name" in entry
            assert "temperature" in entry

    @pytest.mark.asyncio
    @patch("extract.aiohttp.ClientSession.get")
    async def test_fetch_plant_data_http_error(self, mock_get):
        """ Tests that http error raised when fetching non existent plant """
        mock_response = AsyncMock()
        mock_response.status = 404  # 404 not found error
        mock_get.return_value = mock_response

        async with aiohttp.ClientSession() as session:
            result = await fetch_plant_data(session, 1)
        assert result is None

    @pytest.mark.asyncio
    @patch("extract.fetch_plant_data", return_value=None)
    async def test_collect_all_plant_data_empty_range(self, mock_fetch_plant_data):
        """ Tests that fetching data is empty """
        async def fetch_empty_data() -> list:
            async with aiohttp.ClientSession() as session:
                return await asyncio.gather(*[])

        result = await fetch_empty_data()
        assert result == []
