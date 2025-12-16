import math

from pymongo import MongoClient

from app.command.import_csv_to_mongodb import CSVImporter
# Ajustez le chemin d'import selon votre structure de projet
from app.config.config import TestingConfig

cfg = TestingConfig.MONGODB_SETTINGS
uri = (f"mongodb://"
       f"{cfg['username']}:{cfg['password']}"
       f"@{cfg['host']}:{cfg['port']}/?authSource=admin"
       ) \
    if cfg['username'] and cfg['password'] \
    else f"mongodb://{cfg['host']}:{cfg['port']}/"
client = MongoClient(uri)
db_name = cfg['db']
db = client[db_name]
collection_name = cfg['collection']
collection = db[collection_name]

TEST_CSV_FILE = 'app/test/import/test_csv_file.csv'


def reset_database():
    print(
        f"Connexion à MongoDB sur {cfg['host']}:{cfg['port']}."
        f" Suppression de la base de données {db_name}...")
    client.drop_database(db_name)

    print("Création d'une collection 'sales_madrid' "
          "pour s'assurer que la base de données est recréée..."
          )
    db.create_collection("sales_madrid")


def insert_data():
    importer = CSVImporter(
        mongo_uri=uri,
        db_name=db_name,
        collection_name=collection_name,
        csv_file_path=TEST_CSV_FILE
    )
    importer.import_csv_to_mongodb()


def dict_contains_subset(superset, subset):
    for key, value in subset.items():
        if key not in superset:
            print("key " + key)
            return False
        if isinstance(value, float) and math.isnan(value):
            if not math.isnan(superset[key]):
                print("val got " + superset[key] + "for key " + key)
                return False
        elif superset[key] != value:
            print("exp val " + str(value) + " for key " +
                  key + " got " + str(superset[key]))
            return False
    return True
