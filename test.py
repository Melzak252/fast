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
        "/login_session", data={"user": login, "password": password})
    assert responde.status_code == 201


def test_token():
    login = "4dm1n"
    password = "NotSoSecurePa$$"
    responde = client.post(
        "/login_token")
    assert responde.status_code == 401
