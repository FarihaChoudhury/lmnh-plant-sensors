"""Connects to the API and extracts relevant information"""

"""Connects to the API and extracts relevant information"""

import requests

def extract_botanist_information(botanist_info: dict):
    """Extracts the botanist information from the API JSON"""
    Botanist = {"name" : "", "email" : "", "phone" : ""}
    for key, value in botanist_info.items():
        if key in Botanist:
            Botanist[key] = value
    return Botanist

def extract_location_information(location_info: list):
    """Extracts the location information from the API JSON"""
    return {"longitude" : location_info[0], 
                "latitude" : location_info[1], 
                "closest_town" : location_info[2], 
                "ISO_code" : location_info[3]
                }

def extract_plant_information(plant_info: dict):
    """Extracts the plant information from the API JSON"""
    Plant = {"name" : "","scientific_name" : "", "original_url" : "", }

def extract_metric_information(metric_info: dict):
    """Extracts the plant metric information from the API JSON"""
    Plant_metric = {}

def store_information(api_information: dict[dict]) -> None:
    """Stores information extracted from the API"""
    Botanist = extract_botanist_information(api_information['botanist'])
    Location = extract_location_information(api_information['origin_location'])
    Plant = extract_plant_information(api_information)
    Plant_metric = extract_metric_information(api_information)

    print(Location)

def connect_to_endpoints() -> None:
    """Connects to an API endpoint"""
    for number in range(50):
        url = f"https://data-eng-plants-api.herokuapp.com/plants/{number}"
        response = requests.get(url)

        if response.status_code == 200:
            #print(response.json())
            store_information(response.json())
        else:
            print(f"Failed with status code: {response.status_code}")
        return

if __name__ == "__main__":
    connect_to_endpoints()