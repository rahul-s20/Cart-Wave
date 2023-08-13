import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_mongoengine import MongoEngine

db = MongoEngine()


def create_app(env='Development'):
    app = Flask(__name__)
    CORS(app)
    # app.config['MONGODB_SETTINGS'] = {
    #     'db': 'cart_wave_de',
    #     'host': '0.0.0.0',
    #     'port': 27017
    # }
    app.config.from_object('configuration.config.%s' % env)

    db.init_app(app)

    from routes.user_route import user_blueprint
    from routes.product_route import product_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(product_blueprint)
    print("App started")

    return app
