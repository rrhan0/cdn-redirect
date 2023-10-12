import pytest
import requests
import os

BASE_URL = os.getenv('HOST', default='http://127.0.0.1:8080')


def test_redirect_https():
    response = requests.get(f'{BASE_URL}/redirect/https://www.cbc.ca/')
    assert response.status_code == 200


def test_redirect_no_https():
    response = requests.get(f'{BASE_URL}/redirect/www.cbc.ca/')
    assert response.status_code == 200

