import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Set secret key from environment
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    
    # Configure for proxy (needed for url_for to generate with https)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Configure upload settings
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get("MAX_UPLOAD_MB", "5")) * 1024 * 1024  # Default 5MB
    app.config['UPLOAD_FOLDER'] = 'temp_uploads'
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register routes
    from routes import main_bp
    app.register_blueprint(main_bp)
    
    return app

app = create_app()
