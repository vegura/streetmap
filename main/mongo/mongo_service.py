from pymongo import MongoClient

import main.mongo.mongo_resources as res
import json

from main.model.model import Order

MONGO_COLLECTION = "Orders"

class MongoOrderDao:
    def __init__(self):
        self.client = MongoClient(res.MONGO_HOST + ":" + str(res.MONGO_PORT))
        self.db = self.client[res.MONGO_DATABASE]
        self.collection = self.db[MONGO_COLLECTION]

        print(f"Connection to database: \n\tHOST: {res.MONGO_HOST}\n\tPORT: {res.MONGO_PORT}")

    def save_order(self, order: json):
        print(f"saving order -> {str(order)}")
        return self.collection.insert_one(order).inserted_id

    def find_order_by_postal_code(self, postal_code: str):
        return self.collection.find_one(self.collection, {"postal_code": postal_code})

    def find_order_by_id(self, id: int):
        return self.collection.find_one({"id": id})
