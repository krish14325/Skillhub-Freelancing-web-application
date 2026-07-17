from flask import Flask 
from app.config import Config
from app.extensions import db , migrate , bcrypt , login_manager
from auth import auth_bp
from freelancer import freelancer_bp
from client import client

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    migrate.init_app(app , db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(freelancer_bp)
    app.register_blueprint(client)
    return app




