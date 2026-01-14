from flask import Flask
from flask_cors import CORS
from app.controller.predict_price import house_price
from app.controller import main

app = Flask(__name__)

# Allow Angular dev server
CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:4200"]}},
    supports_credentials=False,
)

app.register_blueprint(main)
app.register_blueprint(house_price)

