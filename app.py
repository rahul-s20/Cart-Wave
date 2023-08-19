import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_mongoengine import MongoEngine

from routes.user_route import user_blueprint
from routes.product_route import product_blueprint
from routes.order_route import order_blueprint

db = MongoEngine()


def create_app(env='Development'):
    app = Flask(__name__)

    api_v1_cors_config = {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["*"]
    }
    app.config.from_object('configuration.config.%s' % env)
    db.init_app(app)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(order_blueprint)
    CORS(app, resources={r'*': api_v1_cors_config}, support_credentials=True)
    print("App started")

    return app
