from flask import jsonify
from . import stats_bp
from app.service.stats.correlation_service import CorrelationService


@stats_bp.route("/correlation/buy-price", methods=["GET"])
def get_buy_price_correlation_matrix():
    service = CorrelationService()
    matrix = service.get_buy_price_correlation_matrix()
    return jsonify(matrix), 200
