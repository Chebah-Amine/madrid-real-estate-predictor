from typing import Optional, Dict, Any
from app.config.extensions import get_collection
from app.repository.stats.correlation_repository import CorrelationRepository
from app.exceptions.stats import NoDataFoundException

class CorrelationService:  
    def __init__(self):
        self.collection = get_collection()
        self.repository = CorrelationRepository()
        
    def get_buy_price_correlation_matrix(self) -> Optional[Dict[str, Any]]:
        result = self.repository.get_buy_price_correlation_matrix(features=["n_rooms", "sq_mt_built", "n_bathrooms"])

        if result is None:
            raise NoDataFoundException(request_desc="Get buy price correlation matrix")
        
        return result