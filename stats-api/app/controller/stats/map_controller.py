from flask import jsonify
from . import stats_bp
from app.service.stats.map_service import MapService

@stats_bp.route('/map/mean-price/neighborhood', methods=['GET'])
def get_mean_price_by_neighborhood():
    service = MapService()
    mean_price_by_neighborhood = service.get_mean_price_by_neighborhood()
    return jsonify(mean_price_by_neighborhood)
