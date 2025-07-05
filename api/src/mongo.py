import pymongo
from pymongo.collection import Collection
import uuid
import os

import pymongo.collection

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_URI = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@mongo:27017'

client = pymongo.MongoClient(MONGO_URI)
collection : Collection = client['citric-sheep']['elevator-logs']

# CRUD
def create_log(log : dict):
    log['trip_id'] = str(uuid.uuid1())
    collection.insert_one(log)

def read_log(trip_id : str):
    doc = collection.find_one({'trip_id' : trip_id})
    return doc

def delete_log(trip_id : str):
    doc = collection.find_one_and_delete({'trip_id' : trip_id})
    return doc

def read_all():
    docs = collection.find({}, {'_id' : 0})
    return list(docs)