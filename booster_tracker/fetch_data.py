import requests
from .models import Launch


def fetch_nxsf_launches() -> list:
    url = "https://nextspaceflight.com/api/launches/"
    response = requests.get(url)
    return response.json()["list"]


def fetch_nxsf_recovery() -> list:
    url = "https://nextspaceflight.com/api/recoveries/"
    response = requests.get(url)
    return response.json()["list"]


def fetch_nxsf_boosters() -> list:
    url = "https://nextspaceflight.com/api/reusable_vehicles"
    response = requests.get(url)
    return response.json()["list"]


def fetch_nxsf_pads() -> list:
    url = "https://nextspaceflight.com/api/pads/"
    response = requests.get(url)
    return response.json()["list"]
