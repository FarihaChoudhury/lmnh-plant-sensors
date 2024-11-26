import pytest
from extract import extract_botanist_information, extract_location_information, extract_metric_information, extract_plant_information, fetch_and_collect_data, write_to_csv


@pytest.fixture
def sample_api_information():
    return {
        "botanist": {
            "email": "test@test.com",
            "name": "firstname lastname",
            "phone": "+0000 111222"
        },
        "images": {
            "original_url": "https://test.jpg",
        },
        "last_watered": "Test time 1",
        "name": "Test Test",
        "origin_location": [
            "1",
            "0",
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


def test_extract_botanist_information():
    input_data = {"name": "firstname lastnam",
                  "email": "test@test.com", "phone": "+0000 111222"}
    output_data = {"name": "firstname lastnam",
                   "email": "test@test.com", "phone": "+0000 111222"}
    assert extract_botanist_information(input_data) == output_data


def test_extract_location_information():
    input_data = ["1", "0", "London", "GB"]
    output_data = {"longitude": "1", "latitude": "0",
                   "closest_town": "London", "ISO_code": "GB"}
    assert extract_location_information(input_data) == output_data


def test_extract_metric_information():
    input_data = {"temperature": 0,
                  "soil_moisture": 0,
                  "recording_taken": "Test time 2",
                  "last_watered": "Test time 1"}
    output_data = {"temperature": 0,
                   "soil_moisture": 0,
                   "recording_taken": "Test time 2",
                   "last_watered": "Test time 1"}
    assert extract_metric_information(input_data) == output_data


def test_extract_plant_information():
    input_data = {"name": "Test Test", "scientific_name": ["Test Test"],
                  "images": {"original_url": "https://test.jpg"}}
    output_data = {"name": "Test Test", "scientific_name": "Test Test",
                   "original_url": "https://test.jpg"}
    assert extract_plant_information(input_data) == output_data
