# database/mongo.py

from pymongo import MongoClient
from app.core.config import get_settings

# Load settings
settings = get_settings()

try:
    # Establish MongoDB connection using the settings
    mongo_client = MongoClient(settings.MONGO_URI)
    mongo_db = mongo_client[settings.MONGO_DB_NAME]
    
    # Ping the database to ensure the connection is successful
    mongo_client.admin.command("ping")
    print("✅ MongoDB Connection Successful")
    print(mongo_client)  # Should say <pymongo.mongo_client.MongoClient object ...>
    print(mongo_db)      # Should say <pymongo.database.Database object ...>
    # List existing collections for debugging purposes
    collections = mongo_db.list_collection_names()
    print("📂 Existing collections:", collections)

except Exception as e:
    print("❌ MongoDB Connection Failed:", e)
    raise e


#checkpointer = MongoDBSaver(mongo_db, collection_name="hitl_checkpoints")
#from langgraph.checkpoint.mongodb import MongoDBSaver
from database.mongo import mongo_db
