# services/mongo_service.py
from typing import Any, Dict
from database.mongo import mongo_db

class MongoStateStore:
    def __init__(self):
        self.db = mongo_db  # Use shared connection

    def create_thread(self, thread_id: str, initial_state: Dict[str, Any]) -> None:
        """
        Create a new conversation 'thread' record.
        """
        self.db["threads"].insert_one({
            "thread_id": thread_id,
            **initial_state
        })

    def update_thread(self, thread_id: str, update_data: Dict[str, Any]) -> None:
        """
        Update an existing thread.
        """
        self.db["threads"].update_one(
            {"thread_id": thread_id},
            {"$set": update_data},
            upsert=True
        )

    def load_thread(self, thread_id: str) -> Dict[str, Any]:
        """
        Load thread data from DB. Returns an empty dict if not found.
        """
        doc = self.db["threads"].find_one({"thread_id": thread_id})
        return doc if doc else {}
    