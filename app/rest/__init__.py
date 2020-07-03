from flask import Blueprint
from flask_restx import Api

api = Api(version='1.0', title='Predictor API',
          description='Discount Predictor')

bp = Blueprint('api', __name__)

api.init_app(bp)

from app.rest import controller