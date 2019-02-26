from app.blueprints import app_blueprints
from app.models.__init__ import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from importlib import import_module
import json
import os


def get_app():
    # Load Environment Variables
    load_dotenv(dotenv_path='app/.env')

    # Create Flask App
    app = Flask(__name__)
    app.template_folder = app.root_path + '/templates'
    app.static_folder = app.root_path + '/static'

    # Flask Config
    app.config['SESSION_COOKIE_SECURE'] = True
    app.secret_key = os.getenv('SECRET_KEY')
    app.url_map.strict_slashes = False
    app.add_url_rule(
        '/favicon.ico',
        'favicon',
        lambda: app.send_static_file('favicon.ico')
    )
    app.add_url_rule(
        '/robots.txt',
        'robots',
        lambda: app.send_static_file('robots.txt')
    )
    app.add_url_rule(
        '/sitemap.xml',
        'sitemap',
        lambda: app.send_static_file('sitemap.xml')
    )

    # Database Config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Intialize Database
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # Import Blueprints
    for blue in app_blueprints:
        import_module(blue.import_name)
        app.register_blueprint(blue)

    return app
