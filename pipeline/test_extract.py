"""Tests for extract.py"""
#  pylint: skip-file

import pytest
from unittest.mock import patch, mock_open, AsyncMock

from extract import (extract_botanist_information,
                     extract_location_information,
                     extract_metric_information,
                     extract_plant_information,
                     fetch_and_collect_data,
                     write_to_csv)


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


@patch("extract.open", new_callable=mock_open)
def test_write_to_csv(mock_open, sample_api_information):
    data = [
        {
            "name": "Test Test",
            "email": "test@test.com",
            "phone": "+0000 111222",
            "latitude": "1",
            "longitude": "0",
            "closest_town": "London",
            "ISO_code": "GB",
            "plant_name": "Test Test",
            "plant_scientific_name": "Test Test",
            "plant_image_url": "https://test.jpg",
            "temperature": 0,
            "soil_moisture": 1,
            "recording_taken": "Test time 2",
            "last_watered": "Test time 1"
        }
    ]
    write_to_csv(data, "test.csv")
    handle = mock_open()
    handle.write.assert_any_call(
        "name,email,phone,latitude,longitude,closest_town,ISO_code,plant_name,plant_scientific_name,plant_image_url,temperature,soil_moisture,recording_taken,last_watered\r\n"
    )
    handle.write.assert_any_call(
        "Test Test,test@test.com,+0000 111222,1,0,London,GB,Test Test,Test Test,https://test.jpg,0,1,Test time 2,Test time 1\r\n"
    )
