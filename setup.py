"""
HRMS Lite — Admin Setup & Seed Script
--------------------------------------
Run this ONCE after setting up the project to:
  1. Create MongoDB indexes (unique constraints)
  2. Create the default admin user

Usage:
    python setup.py

Override credentials via .env:
    ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_NAME
"""

import asyncio
import os
import hashlib
import secrets
from dotenv import load_dotenv

load_dotenv()

# Import the single shared DB connection
from database import client, db, admins_collection

# ── Admin credentials from .env ───────────────────────────────────
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")
ADMIN_FULL_NAME = os.getenv("ADMIN_NAME", "System Administrator")
# ─────────────────────────────────────────────────────────────────


def hash_password(password: str) -> str:
    """SHA-256 hash with a random salt."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}:{hashed}"


async def setup():
    print("\n🚀  HRMS Lite — Setup Script")
    print("=" * 40)

    # ── 1. Create indexes ─────────────────────────────────────────
    print("\n📌  Creating database indexes...")

    await db["employees"].create_index("employee_id", unique=True)
    await db["employees"].create_index("email", unique=True)
    print("  ✅  employees.employee_id  (unique)")
    print("  ✅  employees.email        (unique)")

    await db["attendance"].create_index(
        [("employee_id", 1), ("date", 1)], unique=True
    )
    print("  ✅  attendance.(employee_id + date)  (unique compound)")

    await db["admins"].create_index("username", unique=True)
    print("  ✅  admins.username  (unique)")

    # ── 2. Create admin user ──────────────────────────────────────
    print("\n👤  Setting up admin user...")

    existing = await admins_collection.find_one({"username": ADMIN_USERNAME})
    if existing:
        print(f"  ⚠️   Admin '{ADMIN_USERNAME}' already exists — skipping creation.")
    else:
        await admins_collection.insert_one({
            "username": ADMIN_USERNAME,
            "password_hash": hash_password(ADMIN_PASSWORD),
            "full_name": ADMIN_FULL_NAME,
            "role": "admin",
        })
        print(f"  ✅  Admin user created successfully!")
        print(f"\n  ┌─────────────────────────────────┐")
        print(f"  │  Username : {ADMIN_USERNAME:<22}│")
        print(f"  │  Password : {ADMIN_PASSWORD:<22}│")
        print(f"  │  Role     : admin                 │")
        print(f"  └─────────────────────────────────┘")
        print(f"\n  ⚠️   Change your password after first login!")

    client.close()

    print("\n✅  Setup complete! You can now start the server:")
    print("    uvicorn main:app --reload --port 8000\n")


if __name__ == "__main__":
    asyncio.run(setup())
