# db/mongo.py
# shared database connection pattern creates a single MongoDB client instance 

from pymongo import MongoClient
from app.core.config import get_settings

# Load settings
settings = get_settings()

# Create a single shared MongoDB client
mongo_client = MongoClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB_NAME]

def test_connection():
    """Ping MongoDB to check if it's available."""
    return mongo_client.admin.command("ping")