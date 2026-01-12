from flask import Blueprint, jsonify
from app.service.sales_service import SalesService

sales_bp = Blueprint('sales_bp', __name__, url_prefix='/sales')


@sales_bp.route('/<sale_id>', methods=['GET'])
def get_sale(sale_id):
    try:
        service = SalesService()
        sale = service.get_sale_by_id(sale_id)
        if sale:
            return jsonify(sale)
        else:
            return jsonify({"error": "Sale not found " + sale_id}), 404
    except Exception as e:
        return jsonify(
            {"error": "An unexpected error occurred", "details": str(e)}), 500
