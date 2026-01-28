from flask import Flask
from flask_cors import CORS
from app.config.extensions import init_mongo
from app.config.settings import config
from app.controller.sales_controller import sales_bp
from app.controller.stats import stats_bp
from app.controller import main
from .errors import register_error_handlers


def create_app(config_name="development"):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config[config_name])

    # Allow Angular dev server
    CORS(
        app,
        resources={r"/*": {"origins": ["http://localhost:4200"]}},
        supports_credentials=False,
    )

    # Initialize extensions
    init_mongo(app)

    register_error_handlers(app)

    # Save blueprints (roots, controller)
    app.register_blueprint(main)
    app.register_blueprint(sales_bp)
    app.register_blueprint(stats_bp)

    with app.app_context():
        app.logger.info(f"App started in {config_name} mode")
        app.logger.info(
            f"MongoDB: {app.config['MONGODB_HOST']}:{app.config['MONGODB_PORT']}"
        )

    return app
