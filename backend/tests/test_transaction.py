import os
import pytest
import random
from datetime import timedelta, datetime
from decimal import Decimal
from pymongo import MongoClient
from fastapi.testclient import TestClient
from main import app
from dependencies.settings import settings
from auth.data_util import create_access_token
from tests.dumps import user_template, random_transactions
from tests.common import BASE_ROUTE


os.environ["MONGODB_DB_NAME"] = os.environ["MONGODB_TEST_DB"]


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user(client):
    res = client.post(f"{BASE_ROUTE}/user/sign_up", json=user_template)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_template["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(
        data={"sub": test_user["_id"]}, expires_delta=timedelta(minutes=30)
    )


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


# Test cases for /api/v1/transaction/create
def test_create_transaction(authorized_client):
    transaction = random.choice(random_transactions)
    response = authorized_client.post(
        f"{BASE_ROUTE}/transaction/create", json=transaction
    )
    assert response.status_code == 201
    response_json = response.json()

    assert "_id" in response_json, "User ID not found in response"
    assert "user_id" in response_json, "User ID not found in response"
    assert "display_amount" in response_json, "Display amount not found in response"
    assert "created" in response_json, "Created timestamp not found in response"
    assert (
        "last_modified" in response_json
    ), "Last modified timestamp not found in response"

    response_decimal = response_json["amount"].split(".")[1]
    request_decimal = transaction["amount"].split(".")[1]
    assert response_decimal == request_decimal
    assert len(response_decimal) == len(request_decimal)
    assert int(response_decimal) == int(request_decimal)


# Test cases for /api/v1/transaction/all
def test_get_transactions(authorized_client):
    for i in range(5):
        authorized_client.post(
            f"{BASE_ROUTE}/transaction/create", json=random.choice(random_transactions)
        )
    response = authorized_client.get(f"{BASE_ROUTE}/transaction/all")

    assert response.status_code == 200
    response_json = response.json()

    assert len(response_json) == 5


# Test cases for /api/v1/transaction/update
def test_update_transaction(authorized_client):
    transaction = random.choice(random_transactions)
    res = authorized_client.post(f"{BASE_ROUTE}/transaction/create", json=transaction)
    updates = {
        "transaction_type": "credit",
        "status": "pending",
        "display_amount": "$89.47",
    }
    response = authorized_client.put(
        f"{BASE_ROUTE}/transaction/update/{res.json()['_id']}",
        json=updates,
    )
    assert response.status_code == 202
    response_json = response.json()
    assert "_id" in response_json, "User ID not found in response"
    assert "user_id" in response_json, "User ID not found in response"
    assert "display_amount" in response_json, "Display amount not found in response"
    assert "created" in response_json, "Created timestamp not found in response"
    assert (
        "last_modified" in response_json
    ), "Last modified timestamp not found in response"

    assert res.json()["_id"] == response_json["_id"]
    assert res.json()["last_modified"] != response_json["last_modified"]

    response_decimal = response_json["amount"].split(".")[1]
    request_decimal = transaction["amount"].split(".")[1]
    assert response_decimal == request_decimal
    assert len(response_decimal) == len(request_decimal)
    assert int(response_decimal) == int(request_decimal)


# Test cases for /api/v1/transaction/delete
def test_delete_transaction(authorized_client):
    transaction = random.choice(random_transactions)
    res = authorized_client.post(f"{BASE_ROUTE}/transaction/create", json=transaction)

    response = authorized_client.delete(
        f"{BASE_ROUTE}/transaction/delete/{res.json()['_id']}"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "success"


# Test cases for /api/v1/transaction/analytics
def test_analyse_records(authorized_client, test_user):
    amounts = []
    for i in range(5):
        transaction = random.choice(random_transactions)
        amounts.append(Decimal(transaction["amount"]))
        authorized_client.post(f"{BASE_ROUTE}/transaction/create", json=transaction)
    response = authorized_client.get(
        f"{BASE_ROUTE}/transaction/analytics/{test_user['_id']}"
    )
    assert response.status_code == 200
    total_sum = Decimal("0")
    for amount in amounts:
        total_sum = total_sum + Decimal(amount)

    average_spend: Decimal = total_sum / Decimal("5")

    response_json = response.json()

    assert Decimal(response_json["average_transaction_value"]) == average_spend

    assert (
        response_json["day_with_highest_transactions"]
        == datetime.utcnow().date().isoformat()
    )


# Test cases for /api/v1/transaction/{record_id}
def test_get_transaction(authorized_client):
    transaction = random.choice(random_transactions)
    response = authorized_client.post(
        f"{BASE_ROUTE}/transaction/create", json=transaction
    )
    response = authorized_client.get(
        f"{BASE_ROUTE}/transaction/{response.json()['_id']}"
    )
    assert response.status_code == 200

    response_json = response.json()

    assert "_id" in response_json, "User ID not found in response"
    assert "user_id" in response_json, "User ID not found in response"
    assert "display_amount" in response_json, "Display amount not found in response"
    assert "created" in response_json, "Created timestamp not found in response"
    assert (
        "last_modified" in response_json
    ), "Last modified timestamp not found in response"

    response_decimal = response_json["amount"].split(".")[1]
    request_decimal = transaction["amount"].split(".")[1]
    assert response_decimal == request_decimal
    assert len(response_decimal) == len(request_decimal)
    assert int(response_decimal) == int(request_decimal)


# Cleanup function to clear the database after each run
@pytest.fixture(autouse=True)
def finalizer(request):
    client = MongoClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    db.users.delete_many({})
    client.close()
