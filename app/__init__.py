from flask import Flask
from app.controller.predict_price import house_price
from app.controller import main

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(house_price)

