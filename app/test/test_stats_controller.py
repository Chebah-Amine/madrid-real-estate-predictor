from unittest import mock

from flask_testing import TestCase

from app import create_app
from app.test import insert_data, reset_database, dict_contains_subset


class TestStatsController(TestCase):

    @classmethod
    def create_app(cls):
        return create_app('testing')

    @classmethod
    def setUp(cls):
        print("DEBUT TEST CONTROLLER STATISTIQUES")
        insert_data()

    @classmethod
    def tearDown(cls):
        print("FIN TEST CONTROLLER STATISTIQUES")
        reset_database()

    expected_values = [
        {
            "quartier": "San Cristóbal, Madrid",
            "mean_price": 117500.0,
            "latitude": 40.3423454,
            "longitude": -3.6872259
        },
        {
            "quartier": "San Andrés, Madrid",
            "mean_price": 144247.0,
            "latitude": 40.3446298,
            "longitude": -3.7151909
        }
    ]

    def test_get_mean_price_by_neighborhood(self):
        response = self.client.get('/stats/map/mean-price/neighborhood')

        self.assert200(
            response,
            "La requête doit réussir avec un statut 200"
        )

        response_data = response.json
        print(response_data)
        response_data_sorted = sorted(
            response_data, key=lambda x: x['quartier'])
        expected_values_sorted = sorted(
            self.expected_values,
            key=lambda x: x['quartier'])
        for index, value in enumerate(response_data_sorted):
            self.assertTrue(
                dict_contains_subset(
                    {key: value[key] for key in sorted(value)},
                    {
                        key: expected_values_sorted[index][key]
                        for key in sorted(expected_values_sorted[index])
                    }
                )
            )

    def test_get_mean_price_by_neighborhood_no_data(self):
        # Simuler un scénario où il n'y a pas de données
        reset_database()

        response = self.client.get('/stats/map/mean-price/neighborhood')

        self.assert404(
            response,
            "La requête doit échouer avec un statut "
            "404 en l'absence de données"
        )

        # Vérifier le message d'erreur retourné
        data = response.json
        self.assertEqual(
            data,
            {"message": "No neighborhood data available"},
            "Le message d'erreur doit indiquer l'absence de données"
        )

    def test_get_mean_price_by_neighborhood_error(self):
        # Pour cet exemple, imaginons que nous avons mocké un service de
        # manière à ce qu'il lève une exception
        with mock.patch(
                'app.service.stats_service.StatsService.'
                'get_mean_price_by_neighborhood',
                side_effect=Exception("Unexpected error")
        ):
            response = self.client.get('/stats/map/mean-price/neighborhood')

            self.assertEqual(
                response.status_code,
                500,
                "La requête doit échouer avec un statut"
                " 500 en cas d'erreur interne"
            )

            data = response.get_json()
            self.assertEqual(
                data,
                {
                    "error": "An unexpected error occurred",
                    "details": "Unexpected error"
                },
                "Le message d'erreur doit indiquer une erreur inattendue"
            )
