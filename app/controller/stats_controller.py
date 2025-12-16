from flask import Blueprint, jsonify

from app.service.stats_service import StatsService

stats_bp = Blueprint('stats_bp', __name__, url_prefix='/stats')


@stats_bp.route('/map/mean-price/neighborhood', methods=['GET'])
def get_mean_price_by_neighborhood():
    service = StatsService()
    try:
        mean_price_by_neighborhood = service.get_mean_price_by_neighborhood()
        if mean_price_by_neighborhood:
            return jsonify(mean_price_by_neighborhood)
        else:
            return jsonify({"message": "No neighborhood data available"}), 404
    except Exception as e:
        return jsonify(
            {"error": "An unexpected error occurred", "details": str(e)}), 500
