import os
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default='http://localhost:3030')
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default='http://localhost:5050/')


def get_request(endpoint, **kwargs):
    request_url = backend_url.rstrip('/') + '/' + endpoint.lstrip('/')
    response = requests.get(request_url, timeout=15, **kwargs)
    response.raise_for_status()
    return response.json()


def analyze_review_sentiments(text):
    encoded_text = quote(text)
    request_url = sentiment_analyzer_url.rstrip('/') + '/analyze/' + encoded_text
    response = requests.get(request_url, timeout=15)
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict):
        return payload.get('sentiment', 'neutral')
    return 'neutral'


def post_review(data_dict):
    response = requests.post(
        backend_url.rstrip('/') + '/insert_review',
        json=data_dict,
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
