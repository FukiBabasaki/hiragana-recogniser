import os 
from flask_cors import CORS
from flask import Flask

def create_app(test_config=None):
    app_ = Flask(__name__, instance_relative_config=True)
    CORS(app_, support_credentials=True)
    from . import app
    app_.register_blueprint(app.bp)
    app_.config["TEMPLATES_AUTO_RELOAD"] = True

    return app_

if __name__ == "__main__":
    pass
