from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# local import
from instance.config import app_config

# initialize SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    from app.models import Users
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

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
                    
            
        


    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.data.get('email')
        print(data)

        email = request.data.get('email')
        name = request.data.get('name')
        password = request.data.get('password')


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
        

    @app.route('/auth/login', methods=['POST'])
    def login():
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))

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
    

    @app.route('/users', methods=['GET'])
    def users():
        users = Users.query.all()
        results = []

        for user in users:
            obj = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'date_created': user.date_created,
                'date_modified': user.date_modified
            }

            results.append(obj)

        response = jsonify(results)
        response.status_code = 200

        return response

    @app.route('/users/<int:id>', methods=['GET'])
    def get_user(id):
        user = Users.query.filter_by(id=id).first()

        if not user:
            abort(404)

        response = jsonify({
            'id': user.id,
            'name': user.name,
            'email':user.email,
            'role': user.role,
            'date_created': user.date_created,
            'date_modified': user.date_modified
        })
        response.status_code = 200
        return response

    @app.route('/users/<int:id>', methods=['PUT'])
    def edit_user(id):
        user = Users.query.filter_by(id=id).first()

        if not user:
            abort(404)
        user.name = str(request.data.get('name'))
        user.email = str(request.data.get('email'))
        user.role = str(request.data.get('role'))

        user.save()
        response = jsonify({
            'id': user.id,
            'name': str(request.data.get('name')),
            'msg': 'Update successful'
        })
        response.status_code = 200

        return response



    return app