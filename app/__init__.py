import jwt
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS
# local import
from instance.config import app_config


# initialize SQLAlchemy
config_name = os.getenv('APP_SETTINGS')
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[config_name])
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
CORS(app)

from app.auth.view import auth
from app.restaurant.view import partner

# Register Blueprints
app.register_blueprint(auth, url_prefix='/api-v0/auth')
app.register_blueprint(partner, url_prefix='/api-v0/restaurant')