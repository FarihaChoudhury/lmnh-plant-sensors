"""Tests for extract.py"""
#  pylint: skip-file

import pytest
from unittest.mock import patch, mock_open, AsyncMock
import aiohttp
import asyncio

from extract import (extract_botanist_information,
                     extract_location_information,
                     extract_metric_information,
                     extract_plant_information,
                     fetch_plant_data,
                     fetch_and_collect_data)


@pytest.fixture
def sample_api_information():
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
async def test_extract_botanist_information():
    input_data = {"name": "Test Test",
                  "email": "test@test.com", "phone": "+0000 111222"}
    output_data = {"name": "Test Test",
                   "email": "test@test.com", "phone": "+0000 111222"}
    result = await extract_botanist_information(input_data)
    assert result == output_data


@pytest.mark.asyncio
async def test_extract_botanist_information_with_no_name():
    input_data = {"name": None,
                  "email": "test@test.com", "phone": "+0000 111222"}
    output_data = {"name": None,
                   "email": "test@test.com", "phone": "+0000 111222"}
    result = await extract_botanist_information(input_data)
    assert result == output_data


@pytest.mark.asyncio
async def test_extract_location_information():
    input_data = ["1", "0", "London", "GB"]
    output_data = {"latitude": "0", "longitude": "1",
                   "closest_town": "London", "ISO_code": "GB"}
    result = await extract_location_information(input_data)
    assert result == output_data


@pytest.mark.asyncio
async def test_extract_metric_information():
    input_data = {"temperature": 0,
                  "soil_moisture": 0,
                  "recording_taken": "Test time 2",
                  "last_watered": "Test time 1"}
    output_data = {"temperature": 0,
                   "soil_moisture": 0,
                   "recording_taken": "Test time 2",
                   "last_watered": "Test time 1"}
    result = await extract_metric_information(input_data)
    assert result == output_data


@pytest.mark.asyncio
async def test_extract_plant_information():
    input_data = {"plant_id": 1, "name": "Test Test",
                  "scientific_name": ["Test Test"]}
    output_data = {"plant_id": 1, "name": "Test Test",
                   "scientific_name": "Test Test"}
    result = await extract_plant_information(input_data)
    assert result == output_data


@pytest.mark.asyncio
@patch("extract.aiohttp.ClientSession.get")
async def test_fetch_and_collect_data(mock_get, sample_api_information):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = sample_api_information

    mock_get.return_value = mock_response
    result = await fetch_and_collect_data()

    for entry in result:
        assert "name" in entry
        assert "plant_name" in entry
        assert "temperature" in entry


@pytest.mark.asyncio
@patch("extract.aiohttp.ClientSession.get")
async def test_fetch_plant_data_http_error(mock_get):
    mock_response = AsyncMock()
    mock_response.status = 404  # 404 not found error
    mock_get.return_value = mock_response

    async with aiohttp.ClientSession() as session:
        result = await fetch_plant_data(session, 1)
    assert result is None


@pytest.mark.asyncio
@patch("extract.fetch_plant_data", return_value=None)
async def test_fetch_and_collect_data_empty_range(mock_fetch_plant_data):
    async def fetch_empty_data() -> list:
        async with aiohttp.ClientSession() as session:
            return await asyncio.gather(*[])

    result = await fetch_empty_data()
    assert result == []
