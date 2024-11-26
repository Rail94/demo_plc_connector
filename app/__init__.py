from importlib import import_module
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(cors_allowed_origins="*")
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app.config.from_pyfile('config.py')

    login_manager.login_view = 'login'

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register blueprints
    for module_name in ('home', 'files', 'analisis', 'calibration', 'settings', 'socket', 'reports', 'errors', 'pdfs', 'admin'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)
        
    from .socket.routes import start_background_thread
    start_background_thread(app)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from . import models
    return models.Users.query.get(int(user_id))
