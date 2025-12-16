import unittest

from flask import current_app
from flask_testing import TestCase

from app import create_app  # Assurez-vous que ce chemin d'import est correct


# Ajustez le chemin d'import selon votre structure de projet


class MyTestSuite(TestCase):

    def create_app(self):
        """
        Crée une instance de l'application avec la configuration de test.
        """
        app = create_app('testing')
        return app

    def test_app_is_testing_mode(self):
        """
        Vérifie que l'application est en mode test.
        """
        self.assertTrue(current_app.config['TESTING'])
        self.assertFalse(current_app is None)
        self.assertEqual(
            current_app.config['MONGODB_SETTINGS']['db'],
            'sales_test')


if __name__ == '__main__':
    unittest.main()
