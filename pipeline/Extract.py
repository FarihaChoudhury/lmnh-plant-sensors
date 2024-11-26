"""Connects to the API and extracts relevant information"""

import csv
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Logs to console
    ]
)


def extract_botanist_information(botanist_info: dict) -> dict:
    """Extracts the botanist information from the API JSON"""
    return {"name": botanist_info.get('name'),
            "email": botanist_info.get('email'),
            "phone": botanist_info.get('phone')}


def extract_location_information(location_info: list) -> dict:
    """Extracts the location information from the API JSON"""
    return {"longitude": location_info[0],
            "latitude": location_info[1],
            "closest_town": location_info[2],
            "ISO_code": location_info[3]}


def extract_plant_information(plant_info: dict) -> dict:
    """Extracts the plant information from the API JSON"""
    scientific_name = plant_info.get('scientific_name')
    images = plant_info.get('images')

    if scientific_name is not None:
        scientific_name = scientific_name[0]
    else:
        scientific_name = "None"

    if images is not None:
        images = images['original_url']
    else:
        images = "None"

    return {"name": plant_info.get('name'),
            "scientific_name": scientific_name,
            "original_url": images}


def extract_metric_information(metric_info: dict) -> dict:
    """Extracts the plant metric information from the API JSON"""
    return {"temperature": metric_info.get('temperature'),
            "soil_moisture": metric_info.get('soil_moisture'),
            "recording_taken": metric_info.get('recording_taken'),
            "last_watered": metric_info.get('last_watered')}


def fetch_and_collect_data() -> None:
    """Fetches data from the API and returns it as a list of dictionaries"""
    collected__api_data = []
    for number in range(50):
        url = f"https://data-eng-plants-api.herokuapp.com/plants/{number}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            api_information = response.json()
            botanist = extract_botanist_information(
                api_information['botanist'])
            location = extract_location_information(
                api_information['origin_location'])
            plant = extract_plant_information(api_information)
            plant_metric = extract_metric_information(api_information)

            combined_data = {
                **botanist,
                **location,
                "plant_name": plant["name"],
                "plant_scientific_name": plant["scientific_name"],
                "plant_image_url": plant["original_url"],
                **plant_metric
            }

            collected__api_data.append(combined_data)
            logging.info("Processed plant ID: %s", number)
        else:
            logging.error("Failed with status code: %s, plant ID: %s",
                          response.status_code, number)
    return collected__api_data


def write_to_csv(data: list[dict], csv_file: str) -> None:
    """Writes the collected data to the CSV file"""
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    logging.info("Data written to CSV file: %s", csv_file)


if __name__ == "__main__":
    CSV_FILE = "Plant_information.csv"
    collected_data = fetch_and_collect_data()
    write_to_csv(collected_data, CSV_FILE)

{
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
