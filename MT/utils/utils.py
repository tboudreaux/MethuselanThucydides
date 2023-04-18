from MT.config import retrivalAPI_IP, retrivalAPI_Port
from typing import Any, Dict
import requests
import os
import sys


SEARCH_TOP_K = 3

DATABASE_INTERFACE_BEARER_TOKEN = os.environ["BEARER_TOKEN"]


def upsert(id: str, content: str, subject:str):
    """
    Upload one piece of text to the database with associated metadata
    """
    url = f"http://{retrivalAPI_IP}:{retrivalAPI_Port}/upsert"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + DATABASE_INTERFACE_BEARER_TOKEN,
    }

    data = {
        "documents": [{
            "id": id,
            "text": content,
            "metadata": {
                "subject": subject,
            }
        }]
    }
    response = requests.post(url, json=data, headers=headers, timeout=600)

    if response.status_code == 200:
        print("uploaded successfully.")
    else:
        print(f"Error: {response.status_code} {response.content}")
