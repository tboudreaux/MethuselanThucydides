from typing import Any, Dict
import requests
import os
import sys

from config import retrivalAPI_IP, retrivalAPI_Port

SEARCH_TOP_K = 3

DATABASE_INTERFACE_BEARER_TOKEN = os.environ["BEARER_TOKEN"]


def upsert(id: str, content: str, sourceID:str, createdAt: str, author:str, subject:str, source_url: str):
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
                "source_id": sourceID,
                "created_at": createdAt,
                "author": author,
                "subject": subject,
                "source_url": source_url
            }
        }]
    }
    response = requests.post(url, json=data, headers=headers, timeout=600)

    if response.status_code == 200:
        print("uploaded successfully.")
    else:
        print(f"Error: {response.status_code} {response.content}")
