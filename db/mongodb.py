from pymongo import MongoClient
import os

class MongoDB:
    def __init__(self):
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            raise ValueError(
                "MONGODB_URI environment variable is not set. Please provide it in your .env file."
            )
        self.client = MongoClient(mongodb_uri)
        self.db = self.client["drug_discovery"]
    
    def get_collection(self, name):
        return self.db[name]
