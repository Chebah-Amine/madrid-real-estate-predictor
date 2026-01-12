import os
import logging
import math
from typing import Optional, Sequence, Any, Dict

import pandas as pd
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


class CSVImporter:
    """
        Command to import data from CSV to mongo database
    """

    def __init__(self, collection: Collection, logger: Optional[logging.Logger] = None):
        self.collection = collection
        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def nan_to_none(x: Any) -> Any:
        return None if isinstance(x, float) and math.isnan(x) else x

    def import_csv(self, csv_file_path: str):
        try:
            df = pd.read_csv(csv_file_path, sep=",")

            # Replace NaN/NaT with None (Mongo-friendly)
            df = df.where(pd.notna(df), None)

            # Avoid conflict with Mongo "_id"
            if "id" in df.columns:
                df.rename(columns={"id": "_id"}, inplace=True)

            # Convert dataframe to list[dict]
            records: Sequence[Dict[str, Any]] = df.to_dict("records")

            # Ensure no float('nan') survives into Mongo
            docs = [
                {k: CSVImporter.nan_to_none(v) for k, v in rec.items()}
                for rec in records
            ]         

            self.collection.insert_many(docs)

            self.logger.info("Inserted %s documents from %s", len(docs), csv_file_path)

        except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            self.logger.error("Could not import csv file %s: %s", csv_file_path, e)
            raise

        except PyMongoError as e:
            self.logger.error("MongoDB insert failed: %s", e)
            raise

# ---------- Adapter / CLI (no Flask needed) ----------

def build_mongo_client_from_env() -> MongoClient:
    """
    Builds a MongoClient from environment variables.
    """
    host = os.getenv("MONGODB_HOST", "mongodb")
    port = int(os.getenv("MONGODB_PORT", "27017"))

    user = os.getenv("MONGODB_USERNAME") or os.getenv("MONGODB_ROOT_USER")
    pwd = os.getenv("MONGODB_PASSWORD") or os.getenv("MONGODB_ROOT_PASSWORD")
    auth_source = os.getenv("MONGODB_AUTH_SOURCE", "admin")

    if user and pwd:
        return MongoClient(host=host, port=port, username=user, password=pwd, authSource=auth_source)

    return MongoClient(host=host, port=port)


def get_collection_from_env(client: MongoClient) -> Collection:
    db_name = os.getenv("MONGODB_DATABASE", "sales")
    collection_name = os.getenv("MONGODB_COLLECTION", "sales_madrid")
    return client[db_name][collection_name]


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    csv_path = os.getenv("CSV_PATH", "/stats/app/command/import/dataset-back.csv")

    client = build_mongo_client_from_env()
    collection = get_collection_from_env(client)

    importer = CSVImporter(collection=collection)
    importer.import_csv(csv_path)


if __name__ == "__main__":
    main()
