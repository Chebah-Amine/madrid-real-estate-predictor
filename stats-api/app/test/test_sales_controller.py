from app.test.utils import dict_contains_subset

"""
FUNCTIONAL TEST: Test the /sales endpoint to access sales information
"""


class TestSalesController:
    expected_response = {
        "_id": 21742,
        "built_year": 1960.0,
        "buy_price": 85000,
        "buy_price_by_area": 1328,
        "energy_certificate": "D",
        "floor": 3,
        "full_address": "64 Calle de Godella, Madrid, Spain",
        "has_ac": True,
        "has_central_heating": None,
        "has_garden": False,
        "has_green_zones": False,
        "has_individual_heating": None,
        "has_lift": False,
        "has_parking": False,
        "has_pool": False,
        "has_storage_room": False,
        "has_terrace": False,
        "house_type_id": "HouseType 1: Pisos",
        "is_accessible": False,
        "is_exterior": True,
        "is_floor_under": False,
        "is_new_development": False,
        "is_orientation_east": False,
        "is_orientation_north": False,
        "is_orientation_south": False,
        "is_orientation_west": True,
        "is_parking_included_in_price": None,
        "is_renewal_needed": False,
        "latitude": 40.3423454,
        "longitude": -3.6872259,
        "n_bathrooms": 1.0,
        "n_rooms": 2,
        "neighborhood_id": "Neighborhood 135: San Cristóbal (1308.89 €/m2) - District 21: Villaverde",
        "operation": "sale",
        "parking_price": None,
        "raw_address": "Calle de Godella, 64",
        "rent_price": 471,
        "sq_mt_built": 64.0,
        "sq_mt_useful": 60.0,
        "street_name": "Calle de Godella",
        "street_number": 64,
        "title": "Piso en venta en calle de Godella, 64",
    }

    def test_get_sale_found(self, app, mock_mongo_client, client, collection):
        # GIVEN
        app.extensions["mongo_client"] = mock_mongo_client
        collection.insert_one(self.expected_response)

        # WHEN
        response = client.get("/sales/21742")

        # THEN
        assert response.status_code == 200

        response_data = response.get_json()

        assert response_data is not None

        assert dict_contains_subset(response_data, self.expected_response) is True

    def test_get_sale_not_found(self, client):
        # GIVEN / WHEN
        response = client.get("/sales/nonexistent_id")

        # THEN
        assert response.status_code == 404

        assert response.get_json() == {
            "error": "sale_note_found",
            "message": "Sale not found: nonexistent_id",
            "details": {"sale_id": "nonexistent_id"},
        }

    def test_get_sale_error(self, client, monkeypatch):
        # GIVEN
        import app.controller.sales_controller as sales_controller

        # patch the instance method get_sale_by_id, so the signature should be
        # the same
        def boom(self, sale_id):
            raise RuntimeError("DB exploded")

        # Patch the method get_mean_price_by_neighborhood
        monkeypatch.setattr(sales_controller.SalesService, "get_sale_by_id", boom)

        # WHEN
        response = client.get("/sales/not_important")

        # THEN
        assert response.status_code == 500
        assert response.get_json() == {
            "error": "internal_server_error",
            "message": "An unexpected error occured",
            "details": "DB exploded",
        }
