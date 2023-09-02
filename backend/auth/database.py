from passlib.context import CryptContext
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_by_id(id, db):
    entity = await db.find_one({"_id": id})
    if entity is not None:
        return entity
    return None


async def authenticate_user(username, password, db):
    user = await db.find_one({"username": username})
    if not user or not pwd_context.verify(password, user["password"]):
        return False
    return user


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def create_user(user_data, db):
    # Hash the password before storing it, per security requirements.
    user_data.password: str = get_password_hash(user_data.password)

    # Check if the username already exists
    existing_user = await db.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(
            status_code=400, detail="The provided username already registered"
        )

    # Store the user in the database
    new_user = await db.insert_one(user_data.dict())

    user = await get_by_id(new_user.inserted_id, db)

    return user
