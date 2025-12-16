from pymongo import MongoClient

from app.service import get_mongo_config


class SalesService:
    def __init__(self):
        self.mongo_uri, self.db_name, self.collection_name = get_mongo_config()
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def get_sale_by_id(self, sale_id):
        try:
            result = None
            if sale_id.isdigit():
                result = self.collection.find_one({"_id": int(sale_id)})
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
