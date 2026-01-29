from app.repository.stats.map_repository import MapRepository
from app.exceptions.stats import NoDataFoundException


class MapService:
    def __init__(self):
        self.repository = MapRepository()

    def get_mean_price_by_neighborhood(self):
        result = self.repository.get_mean_price_by_neighborhood()

        if result is None:
            raise NoDataFoundException(request_desc="Get mean price by neighborhood")

        return result
