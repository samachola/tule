import os
import datetime
import jwt
from json.decoder import JSONDecodeError
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from flask import Blueprint, request, jsonify, make_response, json, url_for
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from app import app, models

from app.models import Users
#from app.models import Users, Location, Restaurant, Category

auth = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Access Token not available', 'status': False})

        try:
            data = jwt.decode(token, os.getenv('SECRET'))
            current_user = Users.query.filter_by(email=data['email']).first()
        except:
            return jsonify({'message': 'Invalid token', 'status': False})
        return f(current_user, *args, **kwargs)
    return decorated

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data['email']
    name = data['name']
    password = data['password']


    if email.isspace() or name.isspace() or password.isspace():
        response = jsonify({
            'message': 'all fields are required',
            'status': False
        })
        response.status_code = 401
        return response
    else:            
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = Users(email=email, name=name, role='customer', password=hashed_password)
        new_user.save()

        response = jsonify({
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name,
            'role': new_user.role
        })
        response.status_code = 201
        return response
    

@auth.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    email = str(data['email'])
    password = str(data['password'])

    user = Users.query.filter_by(email=email).first()
    
    if user:
        if check_password_hash(user.password, password):
            token = jwt.encode({'email': user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=90)}, os.getenv('SECRET'))
            response = jsonify({
                'message': 'successfully logged in',
                'status': True,
                'token': token.decode('UTF-8')
            })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'message': 'password is incorrect',
                'status': False
            })

            response.status_code = 401
            return response
    else:
        response = jsonify({
            'message': 'user not found',
            'status': False
        })
        response.status_code = 401
        return response
   