from datetime import date, timedelta
from pprint import pprint

from fastapi.testclient import TestClient
import pytest

from main import app

client = TestClient(app)

def test_auth():
    login = "4dm1n"
    password = "NotSoSecurePa$$"
    responde = client.post(
        "/login_session", json={"login": login, "password": password})
    assert responde.status_code == 201

    login = "Melzak"
    password = "Melzak"

    responde = client.post(
        "/login_session", json={"login": login, "password": password})
    assert responde.status_code == 401

    login = ""
    password = "sth"
    responde = client.post(
        "/login_session", json={"login": login, "password": password})
    assert responde.status_code == 401

    login = None
    password = None
    responde = client.post(
        "/login_session", json={"login": login, "password": password})
    assert responde.status_code == 401


def test_token():
    login = "4dm1n"
    password = "NotSoSecurePa$$"
    responde = client.post("/login_token", json={"login": login, "password": password})
    assert responde.status_code == 201
    assert responde.json() == {"token": "AutoryzacjaUzyskana"}

    print("Tutaj1")
    login = "4dm1n1"
    password = "NotSoSecurePa$$"
    responde = client.post("/login_token", json={"login": login, "password": password})
    assert responde.status_code == 401

