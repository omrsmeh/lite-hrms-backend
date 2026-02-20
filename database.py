import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# ── Connection Config ─────────────────────────────────────────────
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "hrms_lite")

# ── Client & Database ─────────────────────────────────────────────
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

# ── Collections (single source of truth for the whole application) ─
employees_collection = db["employees"]
attendance_collection = db["attendance"]
admins_collection = db["admins"]
