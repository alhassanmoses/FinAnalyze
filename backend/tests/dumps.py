import random

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
        "status": random.choice(["pending", "completed", "failed"]),
        "amount": round(random.uniform(100.0, 5000.0), 2),
        "currency": random.choice(["$", "€", "£"]),
        "display_amount": f"${round(random.uniform(100.0, 5000.0), 2)}",
        "user_id": f"{random.randint(100000, 999999)}",
    }
    for _ in range(5)
]

login_data = {
    "username": user_template["username"],
    "password": user_template["password"],
}
