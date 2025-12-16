from flask import Flask

from app.config.config import config
from app.controller.sales_controller import sales_bp
from app.controller.stats_controller import stats_bp
from app.service import set_config_name
from .controller import main


def create_app(config_name):
    app = Flask(__name__)
    set_config_name(config_name)
    app.config.from_object(config[config_name])
    app.register_blueprint(main)
    app.register_blueprint(sales_bp)
    app.register_blueprint(stats_bp)

    return app
