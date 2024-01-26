from src.database import Database, DatabaseEntry
import pymongo
from typing_extensions import Self

class MongoDatabase(Database):
    def __init__(self, connection_string: str, db: str = 'mydatabase', collection: str = 'mycollection') -> None:
        """
        Initialize a MongoDatabase instance.

        Args:
            connection_string (str): The connection string for MongoDB.
            db (str, optional): The name of the database. Defaults to 'mydatabase'.
            collection (str, optional): The name of the collection. Defaults to 'mycollection'.
        """
        # Connect to MongoDB
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db]
        self.collection = self.db[collection]
    
    def create(self, data: DatabaseEntry):
        """
        Create a new document in the collection.

        Args:
            data (DatabaseEntry): The data to be inserted.

        Returns:
            str: The ID of the inserted document.
        """
        return self.collection.insert_one(data.serialize()).inserted_id

    def read(self, id):
        """
        Read a document from the collection.

        Args:
            id: The ID of the document to read.

        Returns:
            dict: The document data.
        """
        return self.collection.find_one({'_id': id})

    def update(self, id, data):
        """
        Update a document in the collection.

        Args:
            id: The ID of the document to update.
            data: The updated data for the document.
        """
        self.collection.update_one({'_id': id}, data)
        print("Document updated successfully.")

    def delete(self, id):
        """
        Delete a document from the collection.

        Args:
            id: The ID of the document to delete.
        """
        self.collection.delete_one({'_id': id})
        print("Document deleted successfully.") 
    
    def delete_all(self):
        """
        Delete all documents from the collection.
        """
        self.collection.delete_many({})
        print("All documents deleted successfully.")

    def read_all_sorted(self):
        """
        Read all documents from the collection, sorted by timestamp in ascending order.

        Returns:
            pymongo.cursor.Cursor: A cursor object containing the sorted documents.
        """
        return self.collection.find().sort('timestamp', pymongo.ASCENDING)
