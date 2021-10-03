import os 

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from . import pred
    app.register_blueprint(pred.bp)

    return app

if __name__ == "__main__":
    pass
