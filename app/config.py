import os
from dotenv import load_dotenv

load_dotenv()

SHARED_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./webhooks.db")
