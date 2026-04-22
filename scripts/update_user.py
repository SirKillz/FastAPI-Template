import json
from pathlib import Path
from alembic import op
from sqlalchemy import text

# Import env vars and overwrite the connection string to the running DB (outside the container service)

import os
from dotenv import load_dotenv
load_dotenv(".env.dev")
os.environ['DATABASE_URL'] = "postgresql+psycopg://app_user:app_password@localhost:5432/app_db"

from fastapi.testclient import TestClient

from app.__main__ import app

client = TestClient(app)

payload = {
    "songs": [
        {
            "id": 1,
            "name": "Living on a prayer",
            "artist": "Bon Jovi",
        }
    ]
}

response = client.put("/users/1", json=payload)
print(response.json())