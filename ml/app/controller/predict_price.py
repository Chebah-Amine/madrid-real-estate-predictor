from flask import Blueprint, request, jsonify
from app.service.predict_price_service import PredictPriceService
from app.controller.utils import validate_input

house_price = Blueprint('house_price', __name__, url_prefix='/predict-house-price')

@house_price.route('/neural-network', methods=['POST'])
def get_price():
    input_house = request.get_json()
    if input_house is None:
        return jsonify({'error': 'No input data provided'}), 400

    is_valid, message = validate_input(input_house)
    if not is_valid:
        return jsonify({'error': message}), 400

    try:
        service = PredictPriceService(input_house)
        price = service.predict_price()
        return jsonify({'predicted_price': price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
