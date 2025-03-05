from flask import Flask
from config import Config
from app.routes import endpoints
from app.database import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(endpoints)

    return app