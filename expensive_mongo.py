import json
import os

from bson import json_util, ObjectId
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')

DATABASE_NAME = 'codeshiba'
COLLECTION_NAME = "expense_tracker"
# 確保環境變數加載正確
print(f'MONGODB_URL: {MONGODB_URL}')  # 調試用

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

# 添加新的用戶到 users 集合
def add_user(username, email, password):
    db = init_mongo()
    users_collection = db['users']

    # 檢查該用戶是否已存在
    if users_collection.find_one({'email': email}):
        return {'error': 'User already exists'}

    # 假設這裡有進行密碼加密處理
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.datetime.utcnow()
    })
    return {'message': 'User registered successfully'}