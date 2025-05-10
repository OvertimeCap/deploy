from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # The route for the login page
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key') # Use environment variable for SECRET_KEY
    
    # Database Configuration for Render (PostgreSQL)
    # Render provides DATABASE_URL environment variable
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///./overtime_dev.db' # Fallback to SQLite for local dev if DATABASE_URL not set
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

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

    with app.app_context():
        db.create_all() # Create tables if they don't exist
        
        # Create admin user only if a specific flag is not set (to avoid issues on Render)
        # Or handle this via a one-time setup script or Render's build commands if needed.
        # For simplicity, let's assume this runs once or is idempotent.
        if not os.environ.get("ADMIN_USER_CREATED"): # Simple flag to prevent re-creation
            admin_email = "overtimecap@gmail.com"
            admin_password = os.environ.get("ADMIN_PASSWORD", "admin_password") # Get admin password from env var
            admin_user = User.query.filter_by(email=admin_email).first()
            if not admin_user:
                admin_user = User(email=admin_email, is_admin=True)
                admin_user.set_password(admin_password) 
                db.session.add(admin_user)
                db.session.commit()
                print(f"Admin user {admin_email} created or already exists.")
                # Potentially set the ADMIN_USER_CREATED flag in a real scenario or manage via migrations

    return app

