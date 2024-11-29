import google.generativeai as genai
import os as environ


def get_plant_fact(plant_name: str) -> str:
    """ Retrieves a fact about a chosen plant based on the plant name. """
    genai.configure(api_key="AIzaSyB016P3WiMFT_A7poTaxZhxyxF45SnVRCk")
    model = genai.GenerativeModel("gemini-pro")

    chat = model.start_chat(history=[])

    response = chat.send_message(
        f"Give me a one sentence fact about {plant_name}", stream=True).to_dict()
    return response['candidates'][0]['content']['parts'][0]['text']


get_plant_fact("lillies")
