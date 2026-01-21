class TestCorrelationController:
    """
    Functional tests for the Matrix Correlation Controller
    """

    def test_get_correlation_matrix_with_success(self, app, mock_mongo_client, collection, client):
        import pandas as pd

        # GIVEN
        app.extensions["mongo_client"] = mock_mongo_client

        test_values = [
            {
                "buy_price": 140000,
                "n_rooms": 3,
                "sq_mt_built": 70,
                "n_bathrooms": 1,
            },
            {
                "buy_price": 20000,
                "n_rooms": 1,
                "sq_mt_built": 25,
                "n_bathrooms": 0,
            },
            {
                "buy_price": 500000,
                "n_rooms": 5,
                "sq_mt_built": 200,
                "n_bathrooms": 3,
            },
        ]

        collection.insert_many(test_values)

        cols = ["buy_price", "n_rooms", "sq_mt_built", "n_bathrooms"]

        df = pd.DataFrame(list(test_values))

        corr = df[cols].corr(method="pearson")

        expected_result = {
            "target": cols[0],
            "features": cols[1:],
            "rows_used": int(len(df)),
            "method": "pearson",
            "matrix": corr.to_dict(),
        }

        # WHEN 
        response = client.get("/stats/correlation/buy-price")

        # THEN
        assert response.status_code == 200
        assert response.get_json() == expected_result 

    
    def test_get_matrix_correlation_error_no_document_found(self, app, mock_mongo_client, client):
        # GIVEN
        app.extensions["mongo_client"] = mock_mongo_client

        # WHEN
        response = client.get("/stats/correlation/buy-price")

        # THEN
        response.status_code == 404
        assert response.get_json() == {
            "error": "no_data_found",
            "message": "No data found",
            "details": {"request_description": "Get buy price correlation matrix"}
        }
        

    def test_get_matrix_correlation_error_only_rows_with_missing_values(self, app, mock_mongo_client, collection, client):
        # GIVEN
        app.extensions["mongo_client"] = mock_mongo_client

        test_values = [
            {
                "buy_price": None,
                "n_rooms": 3,
                "sq_mt_built": 70,
                "n_bathrooms": 1,
            },
            {
                "buy_price": 20000,
                "n_rooms": 1,
                "sq_mt_built": None,
                "n_bathrooms": 0,
            },
            {
                "buy_price": 500000,
                "n_rooms": None,
                "sq_mt_built": 200,
                "n_bathrooms": 3,
            },
        ]

        collection.insert_many(test_values)

        # WHEN
        response = client.get("/stats/correlation/buy-price")

        # THEN
        response.status_code == 404
        assert response.get_json() == {
            "error": "no_data_found",
            "message": "No data found",
            "details": {"request_description": "Get buy price correlation matrix"}
        }

    
    def test_get_matrix_correlation_unexpected_error(self, client, monkeypatch):
        from app.controller.stats import correlation_controller

        # GIVEN
        def boom(self):
            raise RuntimeError("DB exploded")
        
        monkeypatch.setattr(correlation_controller.CorrelationService, "get_buy_price_correlation_matrix", boom)

        # WHEN
        response = client.get("/stats/correlation/buy-price")

        # THEN
        assert response.status_code == 500
        assert response.get_json() == {
            "error": "internal_server_error",
            "message": "An unexpected error occured",
            "details": "DB exploded"
        }


        
