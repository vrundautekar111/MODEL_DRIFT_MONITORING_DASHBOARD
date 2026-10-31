
import os
import requests

API_URL = os.getenv(
    "SALESGUARD_API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


def get(path, timeout=20):
    response = requests.get(
        f"{API_URL}{path}",
        timeout=timeout,
    )

    response.raise_for_status()
    return response.json()


def post(path, payload=None, timeout=180):
    response = requests.post(
        f"{API_URL}{path}",
        json=payload or {},
        timeout=timeout,
    )

    response.raise_for_status()
    return response.json()
