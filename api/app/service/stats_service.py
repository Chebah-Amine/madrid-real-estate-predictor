from pymongo import MongoClient

from app.service import get_mongo_config


class StatsService:
    def __init__(self):
        self.mongo_uri, self.db_name, self.collection_name = get_mongo_config()
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def get_mean_price_by_neighborhood(self):
        pipeline = [
            {
                "$match": {
                    "latitude": {"$ne": None},
                    "longitude": {"$ne": None}
                }
            },
            {
                "$group": {
                    "_id": "$subtitle",
                    "mean_price": {"$avg": "$buy_price"},
                    "first_sale": {"$first": "$$ROOT"}
                }
            },
            {
                "$project": {
                    "quartier": "$_id",
                    "_id": 0,
                    "mean_price": 1,
                    "latitude": "$first_sale.latitude",
                    "longitude": "$first_sale.longitude"
                }
            }
        ]

        result = list(self.collection.aggregate(pipeline))
        return result
