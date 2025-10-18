from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')
    
    # Initialize SocketIO with CORS
    socketio.init_app(app, cors_allowed_origins="*")

    # Register blueprints (if any) — not needed here yet
    from . import routes, events
    app.register_blueprint(routes.bp)
    
    # Attach events to socketio (handled via import side effect)
    events.register_socketio_events(socketio)

    return app