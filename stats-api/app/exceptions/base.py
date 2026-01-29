class CustomException(Exception):
    # Default error
    error_code = "internal_error"
    status_code = 500

    def __init__(self, message, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self):
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
        }
