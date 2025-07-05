import os
from pymongo import MongoClient

def coba(request):
    mongo_uri = os.getenv("MONGOSTRING")

    try:
        client = MongoClient(mongo_uri)
        db = client["mydatabase"]  # ganti dengan nama database kamu
        collection = db["users"]   # ganti dengan nama koleksi kamu

        users = list(collection.find({}, {"_id": 0}).limit(5))  # ambil 5 user, tanpa _id
        return {
            "status": "success",
            "users": users
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
