import os
from pymongo import MongoClient
from flask import jsonify, Request

def coba(request: Request):
    # Tangkap path dari request (karena Cloud Function tidak native pakai Flask routes)
    path = request.path

    # ROUTE 1: Health check
    if path == "/" or path == "/ping":
        return jsonify({"status": "ok", "message": "Cloud Function aktif!"})

    # ROUTE 2: Query MongoDB
    if path == "/users":
        mongo_uri = os.getenv("MONGOSTRING")
        try:
            client = MongoClient(mongo_uri)
            db = client["mydatabase"]
            collection = db["users"]
            users = list(collection.find({}, {"_id": 0}).limit(5))
            return jsonify({"status": "success", "users": users})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    # Default jika path tidak dikenali
    return jsonify({"status": "error", "message": "Route tidak ditemukan."}), 404
