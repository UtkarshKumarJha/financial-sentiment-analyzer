from flask import Flask
from .routes import sentiment_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(sentiment_bp)
    
    return app