class TestMapController:
    """
    Functional tests for Map controller
    """

    def test_get_mean_price_by_neighborhood(self, app, mock_mongo_client, collection, client):
        # GIVEN
        app.extensions["mongo_client"] = mock_mongo_client

        test_values = [
            {
                "_id": 1,
                "buy_price": 140000,
                "subtitle": "San Andrés, Madrid",
                "latitude": 40.3446298,
                "longitude": -3.7151909,
            },
            {
                "_id": 2,
                "buy_price": 20000,
                "subtitle": "San Andrés, Madrid",
                "latitude": None,
                "longitude": None,
            },
            {
                "_id": 3,
                "buy_price": 200000,
                "subtitle": "San Cristóbal, Madrid",
                "latitude": 40.3423454,
                "longitude": -3.6872259,
            },
            {
                "_id": 4,
                "buy_price": 100000,
                "subtitle": "San Cristóbal, Madrid",
                "latitude": 40.3423454,
                "longitude": -3.6872259,
            },
        ]

        expected_values = [
            {
                "neighbor": "San Cristóbal, Madrid",
                "mean_price": 150000.0,
                "latitude": 40.3423454,
                "longitude": -3.6872259,
                "sales_count": 2
            },
            {
                "neighbor": "San Andrés, Madrid",
                "mean_price": 140000.0,
                "latitude": 40.3446298,
                "longitude": -3.7151909,
                "sales_count": 1
            }
        ]       

        collection.insert_many(test_values)

        # WHEN
        response = client.get('/stats/map/mean-price/neighborhood')

        # THEN
        assert collection.count_documents({}) == 4
        assert response.status_code == 200

        response_data = response.json
        response_data_sorted = sorted(response_data, key=lambda x: x['neighbor'])
        expected_values_sorted = sorted(expected_values, key=lambda x: x['neighbor'])
        
        assert len(response_data_sorted) == len(expected_values_sorted)
        
        for index, value in enumerate(response_data_sorted):
            assert {key: value[key] for key in value} \
            == {
                key: expected_values_sorted[index][key]
                for key in expected_values_sorted[index]
            }

    def test_get_mean_price_by_neighborhood_no_data(self, app, mock_mongo_client, collection, client):
        # GIVEN
        app.extensions["mongo_client"] = mock_mongo_client

        # WHEN
        response = client.get('/stats/map/mean-price/neighborhood')

        # THEN
        assert collection.count_documents({}) == 0
        assert response.status_code == 404
        assert response.get_json() == {
            "error": "no_data_found",
            "message": "No data found",
            "details": {"request_description": "Get mean price by neighborhood"}
        }

    def test_get_mean_price_by_neighborhood_error(self, client, monkeypatch):
        # GIVEN 
        import app.controller.stats.map_controller as map_controller

        def boom(self):
            raise RuntimeError("DB exploded")
        
        # Patch the method get_mean_price_by_neighborhood
        monkeypatch.setattr(map_controller.MapService, "get_mean_price_by_neighborhood", boom)

        # WHEN 
        response = client.get("/stats/map/mean-price/neighborhood")

        # THEN
        assert response.status_code == 500
        assert response.get_json() == {
            "error": "internal_server_error",
            "message": "An unexpected error occured",
            "details": "DB exploded"
        }
