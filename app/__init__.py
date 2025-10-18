# app/__init__.py
from flask import Flask, render_template  # ← ADD render_template
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

load_dotenv()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['LLM_API_KEY'] = os.getenv('GROQ_API_KEY')
    app.config['LLM_PROVIDER'] = os.getenv('LLM_PROVIDER', 'groq')

    socketio.init_app(app, cors_allowed_origins="*")

    # ✅ SERVE THE FRONTEND
    @app.route('/')
    def index():
        return render_template('index.html')  # ← This loads your HTML

    # Register SocketIO events
    from . import events
    events.register_socketio_events(socketio)

    return app