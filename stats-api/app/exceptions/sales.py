from .base import CustomException


class SaleNotFoundException(CustomException):
    error_code = "sale_note_found"
    status_code = 404

    def __init__(self, sale_id):
        super().__init__(
            message=f"Sale not found: {sale_id}", details={"sale_id": sale_id}
        )
