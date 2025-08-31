from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["MascotasDB"]

dueños_collection = db["dueños"]
mascotas_collection = db["mascotas"]

def serialize_doc(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc