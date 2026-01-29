from app.exceptions.base import CustomException
from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(CustomException)
    def handle_custom_exception(error: CustomException):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error: Exception):
        response = jsonify(
            {
                "error": "internal_server_error",
                "message": "An unexpected error occured",
                "details": str(error),
            }
        )
        response.status_code = 500
        return response
