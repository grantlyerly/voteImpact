from flask import Flask
from app.methods.config import Config
from app.routes import bp
from . import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with app
    # login_manager.init_app(app)

    db.init_app(app)

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    # import and register blueprints
    app.register_blueprint(bp)
    
    return app