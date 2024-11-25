"""Connects to the API and extracts relevant information"""

import requests

def store_information():
    """Stores information extracted from the API"""

def connect_to_endpoints():
    """Connects to an API endpoint"""
    for number in range(50):
        url = f"https://data-eng-plants-api.herokuapp.com/plants/{number}"
        response = requests.get(url)

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Failed with status code: {response.status_code}")

if __name__ == "__main__":
    connect_to_endpoints()