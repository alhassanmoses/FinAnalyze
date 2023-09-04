# from fastapi.testclient import TestClient
# from main import app
# import json
# from dumps import new_user_data, login_data

# client = TestClient(app)


# # Test cases for /api/v1/user/sign_up
# def test_sign_up():
#     # Test a successful sign-up
#     response = client.post("/api/v1/user/sign_up", json=new_user_data)
#     assert response.status_code == 201
#     assert "access_token" in response.json()
#     assert response.json()["username"] == new_user_data["username"]
#     assert (
#         response.json()["fullname"]
#         == f"{new_user_data['firstname']} {new_user_data['othernames']} {new_user_data['lastname']}"
#     )

#     # Test sign-up with existing username (should fail)
#     response = client.post("/api/v1/user/sign_up", json=new_user_data)
#     assert response.status_code == 400


# # Test cases for /user/login
# def test_login():
#     # Test a successful login
#     response = client.post("/api/v1/user/login", data=login_data)
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#     assert response.json()["username"] == new_user_data["username"]
#     assert (
#         response.json()["fullname"]
#         == f"{new_user_data['firstname']} {new_user_data['othernames']} {new_user_data['lastname']}"
#     )

#     # Test login with incorrect password (should fail)
#     login_data["password"] = "incorrectpassword"
#     response = client.post("/api/v1/user/login", data=login_data)
#     assert response.status_code == 401

#     # Test login with non-existing username (should fail)
#     login_data["username"] = "nonexistentuser"
#     response = client.post("/api/v1/user/login", data=login_data)
#     assert response.status_code == 401
#     print(f"\n\nResponse is ====================== {response} =======================")


# # Run the tests
# if __name__ == "__main__":
#     test_sign_up()
#     test_login()

import os
import pytest
import random
import json
from pymongo import MongoClient
from fastapi.testclient import TestClient
from main import app
from tests.dumps import random_users, login_data, user_template
from dependencies.sharedutils.db import get_database, db
from dependencies.settings import settings

os.environ["MONGODB_DB_NAME"] = os.environ["MONGODB_TEST_DB"]


@pytest.fixture
def client():
    return TestClient(app)


# @pytest.fixture
# def client():
#     return TestClient(app)


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
    login_data["password"] = "incorrectpassword"
    response = client.post("/api/v1/user/login", data=login_data)

    assert response.status_code == 401


def test_login_with_non_existing_username(client):
    login_data["username"] = "nonexistentuser"
    response = client.post("/api/v1/user/login", data=login_data)

    assert response.status_code == 401


# Cleanup function to clear the database after each run
@pytest.fixture(autouse=True)
def finalizer(request):
    client = MongoClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    db.users.delete_many({})
    client.close()
