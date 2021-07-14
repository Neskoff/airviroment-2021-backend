from flask import Blueprint

measurements_bp = Blueprint('measurements', __name__, url_prefix='/api/measurements')
import App.measurements.apis