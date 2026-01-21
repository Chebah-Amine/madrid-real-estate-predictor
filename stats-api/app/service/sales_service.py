import logging
from typing import Optional
from app.repository.sales_repository import SalesRepository
from app.exceptions.sales import SaleNotFoundException

class SalesService:
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.repository = SalesRepository()
        self.logger = logger or logging.getLogger(__name__)

    def get_sale_by_id(self, sale_id):
        sale = self.repository.get_sale_by_id(sale_id)
        
        if sale is None:
            raise SaleNotFoundException(sale_id=sale_id)

        return sale
