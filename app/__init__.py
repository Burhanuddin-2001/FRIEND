from flask import Flask
import os

def create_app(test_config=None):
    """Application Factory Pattern"""
    app = Flask(__name__, instance_relative_config=True)

    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "dev"),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Health Check Endpoint
    @app.route("/health")
    def health_check():
        return {"status": "ok", "message": "Friend is alive"}

    return app
