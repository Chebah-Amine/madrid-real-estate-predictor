from .base import CustomException


class NoDataFoundException(CustomException):
    error_code = "no_data_found"
    status_code = 404

    def __init__(self, request_desc: str | None = None):
        super().__init__(
            message="No data found", details={"request_description": request_desc}
        )
