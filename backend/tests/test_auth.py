import os
import pytest
import random
from pymongo import MongoClient
from fastapi.testclient import TestClient
from main import app
from tests.dumps import random_users
from dependencies.settings import settings

os.environ["MONGODB_DB_NAME"] = os.environ["MONGODB_TEST_DB"]


@pytest.fixture
def client():
    return TestClient(app)


# Test cases for /api/v1/user/sign_up
def test_successful_sign_up(client):
    new_user_data = random.choice(random_users)
    response = client.post("/api/v1/user/sign_up", json=new_user_data)
    assert response.status_code == 201
    assert response.json()["username"] == new_user_data["username"]
    assert (
        response.json()["fullname"]
        == f"{new_user_data['firstname']} {new_user_data['othernames']} {new_user_data['lastname']}"
    )


def test_sign_up_with_existing_username(client):
    new_user_data = random.choice(random_users)
    client.post("/api/v1/user/sign_up", json=new_user_data)
    response = client.post("/api/v1/user/sign_up", json=new_user_data)

    assert response.status_code == 400


# Test cases for /user/login
def test_successful_login(client):
    new_user_data = random.choice(random_users)
    client.post("/api/v1/user/sign_up", json=new_user_data)
    login_data = {
        "username": new_user_data["username"],
        "password": new_user_data["password"],
    }
    response = client.post("/api/v1/user/login", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["username"] == new_user_data["username"]
    assert (
        response.json()["fullname"]
        == f"{new_user_data['firstname']} {new_user_data['othernames']} {new_user_data['lastname']}"
    )


def test_login_with_incorrect_password(client):
    login_data: dict = {"username": "ehcinuw321"}
    login_data["password"] = "ehcinuw321"
    response = client.post("/api/v1/user/login", data=login_data)

    assert response.status_code == 401


def test_login_with_non_existing_username(client):
    login_data: dict = {"password": "ehcinuw321"}
    login_data["username"] = "ehcinuw321"
    response = client.post("/api/v1/user/login", data=login_data)

    assert response.status_code == 401


# Cleanup function to clear the database after each testcase is done running
@pytest.fixture(autouse=True)
def finalizer(request):
    client = MongoClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    db.users.delete_many({})
    client.close()
