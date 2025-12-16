from flask_testing import TestCase

from app import create_app
from app.test import insert_data, reset_database, dict_contains_subset


class TestSalesController(TestCase):

    expected_response = {
        '_id': 21742, 'built_year': 1960.0, 'buy_price': 85000,
        'buy_price_by_area': 1328, 'energy_certificate': 'D',
        'floor': 3, 'full_address': '64 Calle de Godella, Madrid, Spain',
        'has_ac': True, 'has_central_heating': None,
        'has_garden': False,
        'has_green_zones': False, 'has_individual_heating': None,
        'has_lift': False, 'has_parking': False, 'has_pool': False,
        'has_storage_room': False, 'has_terrace': False,
        'house_type_id': 'HouseType 1: Pisos', 'is_accessible': False,
        'is_exterior': True, 'is_floor_under': False,
        'is_new_development': False, 'is_orientation_east': False,
        'is_orientation_north': False, 'is_orientation_south': False,
        'is_orientation_west': True,
        'is_parking_included_in_price': None,
        'is_renewal_needed': False, 'latitude': 40.3423454,
        'longitude': -3.6872259, 'n_bathrooms': 1.0, 'n_rooms': 2,
        'neighborhood_id': 'Neighborhood 135: San Cristóbal (1308.89 €/m2)'
                           ' - District 21: Villaverde',
        'operation': 'sale', 'parking_price': None,
        'raw_address': 'Calle de Godella, 64', 'rent_price': 471,
        'sq_mt_built': 64.0, 'sq_mt_useful': 60.0,
        'street_name': 'Calle de Godella', 'street_number': 64,
        'title': 'Piso en venta en calle de Godella, 64'
    }

    @classmethod
    def create_app(cls):
        return create_app('testing')

    @classmethod
    def setUp(cls):
        print("DEBUT TEST CONTROLLER SALES")
        insert_data()

    @classmethod
    def tearDown(cls):
        print("FIN TEST CONTROLLER SALES")
        reset_database()

    def test_get_sale_found(self):
        response = self.client.get('/sales/21742')
        self.assertEqual(response.status_code, 200)
        response_data = response.json
        self.assertTrue(
            dict_contains_subset(
                response_data,
                self.expected_response
            )
        )

    def test_get_sale_not_found(self):
        response = self.client.get('/sales/nonexistent_id')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json, {
                "error": "Sale not found nonexistent_id"
            }
        )
