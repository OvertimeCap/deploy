from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///overtime.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Definir valores padrão para status_tarefa em registros existentes
        from .models.cliente_potencial import ClientePotencial
        clientes = ClientePotencial.query.all()
        for cliente in clientes:
            if not hasattr(cliente, 'status_tarefa') or cliente.status_tarefa is None:
                cliente.status_tarefa = "pendente"
        db.session.commit()
    
    # User loader function for Flask-Login
    from .models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register Blueprints
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from .routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app
