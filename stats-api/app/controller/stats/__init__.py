from flask import Blueprint

stats_bp = Blueprint("stats_bp", __name__, url_prefix="/stats")

# IMPORTANT: import route modules so routes get registered on stats_bp
from . import map_controller  # noqa: F401
from . import correlation_controller  # noqa: F401
