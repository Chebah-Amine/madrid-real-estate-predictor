from app.config.extensions import get_collection


class MapRepository:
    def __init__(self):
        self.collection = get_collection()

    def get_mean_price_by_neighborhood(self):
        pipeline = [
            # 1) Keep only documents that have usable GPS coordinates and a
            # sale price
            {
                "$match": {
                    "latitude": {"$exists": True, "$ne": None},
                    "longitude": {"$exists": True, "$ne": None},
                    "buy_price": {"$exists": True, "$ne": None},
                }
            },
            # 2) Group by subtitle (neighbor name), compute average sale price,
            # and pick one representative GPS point (deterministic using $avg)
            {
                "$group": {
                    "_id": "$subtitle",  # group key = the neighbor name
                    "avg_buy_price": {"$avg": "$buy_price"},
                    "avg_latitude": {"$avg": "$latitude"},
                    "avg_longitude": {"$avg": "$longitude"},
                    # how many sales contributed
                    "count_sales": {"$sum": 1},
                }
            },
            # 3) Shape the output: rename fields, remove _id, keep only what
            # you want
            {
                "$project": {
                    # exclude col _id
                    "_id": 0,
                    "neighbor": "$_id",
                    "mean_price": "$avg_buy_price",
                    "latitude": "$avg_latitude",
                    "longitude": "$avg_longitude",
                    "sales_count": "$count_sales",
                }
            },
        ]

        result = list(self.collection.aggregate(pipeline))

        return result if len(result) > 0 else None
