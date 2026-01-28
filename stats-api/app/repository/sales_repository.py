from app.config.extensions import get_collection


class SalesRepository:
    def __init__(self):
        self.collection = get_collection()

    def get_sale_by_id(self, sale_id):
        result = None
        if sale_id.isdigit():
            result = self.collection.find_one({"_id": int(sale_id)})
        return result
