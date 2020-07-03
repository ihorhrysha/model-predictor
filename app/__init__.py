from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db=db)
    
    from app.rest import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.frontend import bp as frontend_bp
    app.register_blueprint(frontend_bp)

    return app

# from app import models