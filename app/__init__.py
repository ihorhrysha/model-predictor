from flask import Flask, Blueprint
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

app = Flask(__name__)
app.config.from_object(Config)

# API
api = Api(version='1.0', title='Predictor API',
          description='Discount Predictor')
api_bp = Blueprint('api', __name__, url_prefix='/api')
api.init_app(api_bp)
app.register_blueprint(api_bp)


# frontend
bp = Blueprint('frontend', __name__)
app.register_blueprint(bp)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, routes