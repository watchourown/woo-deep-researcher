# tests/test_mongo.py
import pytest
from database.mongo import mongo_db, test_connection

def test_mongo_connection():
    """Test if MongoDB is accessible by running a ping command."""
    response = test_connection()
    print("MongoDB connection response:")
    print(response)
    assert "ok" in response and response["ok"] == 1.0

def test_insert_and_retrieve():
    """Test inserting and retrieving a document in the test database."""
    test_collection = mongo_db["test_collection"]
    test_doc = {"_id": 1, "name": "Test Document"}
    
    # Insert test document
    test_collection.insert_one(test_doc)

    # Retrieve it
    retrieved_doc = test_collection.find_one({"_id": 1})

    # Assertions
    assert retrieved_doc is not None
    assert retrieved_doc["name"] == "Test Document"

    # Cleanup (delete test data)
    test_collection.delete_one({"_id": 1})