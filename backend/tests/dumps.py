import random
from decimal import Decimal

user_template = {
    "firstname": "Moses",
    "lastname": "Alhassan",
    "othernames": "Wuniche",
    "email": "alhassanmoses.amw@gmail.com",
    "username": "moseswuniche201",
    "password": "moses123",
}

random_users = [
    {
        "firstname": random.choice(["John", "Alice", "David", "Emily", "Michael"]),
        "lastname": random.choice(["Smith", "Johnson", "Williams", "Brown", "Davis"]),
        "othernames": random.choice(["", "Jr.", "Sr."]),
        "email": f"{random.randint(1000, 9999)}randomuser@example.com",
        "username": f"randomuser{random.randint(100, 999)}",
        "password": f"password{random.randint(1000, 9999)}",
    }
    for _ in range(5)
]

random_transactions = [
    {
        "transaction_type": random.choice(["credit", "debit"]),
        "status": random.choice(["pending", "success", "failed", "not_found"]),
        "amount": str(round(random.uniform(100.0, 5000.0), 4)),
        "currency": random.choice(["$", "€", "£"]),
    }
    for _ in range(5)
]
