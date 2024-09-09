import requests


def fetch_nxsf_launches() -> list:
    url = "https://nextspaceflight.com/api/launches/"
    response = requests.get(url)
    return response.json()["list"]
