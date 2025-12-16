import unittest

from mongomock import MongoClient

# Assurez-vous que le chemin d'importation est correct
from app.command.import_csv_to_mongodb import CSVImporter
from app.config.config import TestingConfig

# Création d'un fichier CSV temporaire pour les tests
TEST_CSV_FILE = 'app/test/import/test_csv_file.csv'


class TestCSVImporter(unittest.TestCase):

    expected_keys = [
        "_id",
        "title",
        "sq_mt_built",
        "sq_mt_useful",
        "n_rooms",
        "n_bathrooms",
        "raw_address",
        "street_name",
        "street_number",
        "floor",
        "is_floor_under",
        "neighborhood_id",
        "operation",
        "rent_price",
        "buy_price",
        "buy_price_by_area",
        "house_type_id",
        "is_renewal_needed",
        "is_new_development",
        "built_year",
        "has_central_heating",
        "has_individual_heating",
        "has_ac",
        "has_lift",
        "is_exterior",
        "has_garden",
        "has_pool",
        "has_terrace",
        "has_storage_room",
        "is_accessible",
        "has_green_zones",
        "energy_certificate",
        "has_parking",
        "is_parking_included_in_price",
        "parking_price",
        "is_orientation_north",
        "is_orientation_west",
        "is_orientation_south",
        "is_orientation_east",
        "full_address",
        "latitude",
        "longitude",
        "subtitle"
    ]

    expected_values = [
        {"_id": 21742, "title": "Piso en venta en calle de Godella, 64"},
        {"_id": 21741, "title": "Piso en venta en calle de la"
         " del Manojo de Rosas"},
        {"_id": 21740, "title": "Piso en venta en calle del Talco, 68"}
    ]

    @classmethod
    def setUp(cls):
        print("DEBUT TEST COMMAND IMPORT CSV")

    @classmethod
    def tearDown(cls):
        print("FIN TEST COMMAND IMPORT CSV")

    def test_import_csv_to_mongodb(self):
        # Configuration de test
        cfg = TestingConfig.MONGODB_SETTINGS
        uri = (f"mongodb://"
               f"{cfg['username']}:{cfg['password']}"
               f"@{cfg['host']}:{cfg['port']}/?authSource=admin"
               ) \
            if cfg['username'] and cfg['password'] \
            else f"mongodb://{cfg['host']}:{cfg['port']}/"

        # Utilisation de mongomock pour simuler MongoClient
        mock_client = MongoClient(uri)

        # Injection du client mongomock dans CSVImporter
        importer = CSVImporter(
            mongo_uri=uri,
            db_name=cfg['db'],
            collection_name=cfg['collection'],
            csv_file_path=TEST_CSV_FILE
        )
        # Remplacez le MongoClient par le mongomock
        importer.client = mock_client
        importer.db = importer.client[importer.db_name]
        importer.collection = importer.db[importer.collection_name]

        # Appel de la méthode à tester
        importer.import_csv_to_mongodb()

        # Vérification que les données ont été correctement insérées
        collection = mock_client[cfg['db']][cfg['collection']]
        # Assurez-vous que 2 documents ont été insérés
        self.assertEqual(collection.count_documents({}), 3)
        # Récupère tous les documents de la collection
        documents = list(collection.find({}))

        for index, document in enumerate(documents):
            document_keys = list(document.keys())
            self.assertListEqual(
                sorted(self.expected_keys),
                sorted(document_keys)
            )
            self.assertEqual(
                self.expected_values[index]["_id"],
                document["_id"]
            )
            self.assertEqual(
                self.expected_values[index]["title"],
                document["title"]
            )


if __name__ == '__main__':
    unittest.main()
