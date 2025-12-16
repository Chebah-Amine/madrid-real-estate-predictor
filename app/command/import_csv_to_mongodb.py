import pandas as pd
from pymongo import MongoClient
from app.config.config import Config


class CSVImporter:
    def __init__(self, mongo_uri, db_name, collection_name, csv_file_path):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.csv_file_path = csv_file_path
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def import_csv_to_mongodb(self):
        data = pd.read_csv(self.csv_file_path, sep=",")
        data = data.map(lambda x: None if pd.isna(x) else x)
        if 'id' in data.columns:
            data.rename(columns={'id': '_id'}, inplace=True)
        data_dict = data.to_dict("records")
        self.collection.insert_many(data_dict)
        print(
            f"{len(data_dict)} documents have been inserted into "
            f"{self.db_name}.{self.collection_name}"
        )


if __name__ == "__main__":
    cfg = Config.MONGODB_SETTINGS
    uri = (f"mongodb://"
           f"{cfg['username']}:{cfg['password']}"
           f"@{cfg['host']}:{cfg['port']}/?authSource=admin"
           ) \
        if cfg['username'] and cfg['password'] \
        else f"mongodb://{cfg['host']}:{cfg['port']}/"
    PATH_CSV_FILE = 'app/command/import/dataset-back.csv'
    importer = CSVImporter(
        mongo_uri=uri,
        db_name=cfg['db'],
        collection_name=cfg['collection'],
        csv_file_path=PATH_CSV_FILE
    )
    importer.import_csv_to_mongodb()
