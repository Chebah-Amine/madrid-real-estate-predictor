class TestConfig:
    def test_testing_config_is_loaded(self, app):
        assert app.testing is True
        assert app.config["MONGODB_DATABASE"].endswith("_test")
        assert app.config["MONGODB_COLLECTION"].endswith("_test")
