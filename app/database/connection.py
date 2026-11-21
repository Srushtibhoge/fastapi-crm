
import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

client = None
database = None


async def connect_database():
    global client, database

    mongodb_url = os.getenv("MONGODB_URL")

    if not mongodb_url:
        raise ValueError("MONGODB_URL is missing")

    client = AsyncMongoClient(
        mongodb_url,
        serverSelectionTimeoutMS=5000
    )

    await client.admin.command("ping")

    database = client["ai-crm"]

    print("MongoDB connected successfully")


async def close_database():
    global client, database

    if client:
        await client.close()

    client = None
    database = None


def get_database():
    if database is None:
        raise RuntimeError("Database is not connected")

    return database
