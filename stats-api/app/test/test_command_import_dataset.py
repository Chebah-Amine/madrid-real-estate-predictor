import pandas as pd
import pytest
from pymongo.errors import PyMongoError

"""
INTEGRATION TEST: CSV dataset import into MongoDB (mongomock)
"""


class TestImportCSV:
    """
    Tests for the CSVImporter command/class.
    """

    EXPECTED_KEYS = [
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
        "subtitle",
    ]

    EXPECTED_VALUES = [
        {"_id": 21742, "title": "Piso en venta en calle de Godella, 64"},
        {"_id": 21741, "title": "Piso en venta en calle de la del Manojo de Rosas"},
        {"_id": 21740, "title": "Piso en venta en calle del Talco, 68"},
    ]

    def test_import_csv_with_success(self, csv_importer, collection, test_csv_file):
        # GIVEN / WHEN
        csv_importer.import_csv(str(test_csv_file))

        # THEN
        assert collection.count_documents({}) == 3, "Number of documents should be 3"

        # Use a stable order (by _id) to compare expected values
        documents = list(collection.find({}).sort("_id", -1))

        for index, doc in enumerate(documents):
            assert sorted(doc.keys()) == sorted(self.EXPECTED_KEYS), (
                "Document keys do not match CSV columns"
            )

            expected_id = self.EXPECTED_VALUES[index]["_id"]
            expected_title = self.EXPECTED_VALUES[index]["title"]

            assert doc["_id"] == expected_id, (
                f"Document _id mismatch: {doc['_id']} != {expected_id}"
            )

            assert doc["title"] == expected_title, (
                f"Document title mismatch: {doc['title']} != {expected_title}"
            )

    def test_import_replace_na_with_none(self, populated_collection):
        assert populated_collection.count_documents({}) == 3

        documents = list(populated_collection.find({}))
        for doc in documents:
            assert doc["parking_price"] is None, "parking_price should be None"

    def test_import_csv_file_not_found(self, csv_importer):
        with pytest.raises(FileNotFoundError):
            csv_importer.import_csv("non_existent_file.csv")

    def test_import_csv_empty_file(self, csv_importer, fixtures_dir):
        empty_path = fixtures_dir / "empty.csv"
        with pytest.raises(pd.errors.EmptyDataError):
            csv_importer.import_csv(str(empty_path))

    def test_import_csv_invalid_format(self, csv_importer, fixtures_dir):
        # bad separator ";" instead of ","
        invalid_path = fixtures_dir / "invalid.csv"

        with pytest.raises((pd.errors.ParserError, Exception)):
            csv_importer.import_csv(str(invalid_path))

    def test_import_csv_duplicate_key(self, csv_importer, collection, test_csv_file):
        # First insert
        csv_importer.import_csv(str(test_csv_file))
        count_after_first = collection.count_documents({})

        # Second insert should fail because _id duplicates (mongomock usually
        # raises PyMongoError)
        with pytest.raises(PyMongoError):
            csv_importer.import_csv(str(test_csv_file))

        count_after_second = collection.count_documents({})
        assert count_after_second == count_after_first
