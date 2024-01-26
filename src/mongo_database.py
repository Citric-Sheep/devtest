from src.database import Database, DatabaseEntry
import pymongo
from typing_extensions import Self

class MongoDatabase(Database):
    def __init__(self, connection_string: str, db: str = 'mydatabase', collection: str = 'mycollection') -> None:
        # Connect to MongoDB
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db]
        self.collection = self.db[collection]
    
    def create(self, data: DatabaseEntry):
        return self.collection.insert_one(data.serialize()).inserted_id

    def read(self, id):
        return self.collection.find_one({'_id': id})

    def update(self, id, data):
        self.collection.update_one({'_id': id}, data)
        print("Document updated successfully.")

    def delete(self, id):
        self.collection.delete_one({'_id': id})
        print("Document deleted successfully.") 
    
    def delete_all(self):
        self.collection.delete_many({})
        print("All documents deleted successfully.")

    def read_all_sorted(self):
        return self.collection.find().sort('timestamp', pymongo.ASCENDING)
