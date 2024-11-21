import json
import os

from bson import json_util, ObjectId
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')

DATABASE_NAME = 'codeshiba'
COLLECTION_NAME = "expense_tracker"


def init_mongo():
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    return db


def add_item(name, price, income_type):
    db = init_mongo()
    db.items.insert_one({
        "name": name,
        "price": float(price),
        "type": income_type,
        "date_info": datetime.datetime.utcnow()
    })
    return True


def remove_item(obj_id):
    db = init_mongo()
    db.items.delete_one({
       "_id": ObjectId(obj_id)
    })
    return True


def get_items():
    db = init_mongo()
    cursor = db.items.find()
    return json.loads(json_util.dumps(cursor))
    # return list(cursor)

# print(get_items())
# add_item("牛奶", -100, 'outcome')
# print(get_items())
# remove_item("牛奶", 100)
