from flask import Flask
import os
from dotenv import load_dotenv
from app.extensions import init_supabase

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "dev"),
    )

    if test_config:
        app.config.from_mapping(test_config)

    # ONLY initialize Supabase if we are NOT testing
    if not app.config.get("TESTING"):
        init_supabase()

    @app.route("/health")
    def health_check():
        return {"status": "ok", "message": "Friend is alive"}

    return app