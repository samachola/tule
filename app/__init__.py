from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

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


    @app.route('/auth/register', methods=['POST'])
    def register():
        email = str(request.data.get('email', ''))
        name = str(request.data.get('name', ''))
        password = str(request.data.get('password', ''))

        if email and name and password:
            new_user = Users(email=email, name=name, role='customer', password='password')
            new_user.save()

            response = jsonify({
                'id': new_user.id,
                'email': new_user.email,
                'name': new_user.name,
                'role': new_user.role
            })
            response.status_code = 201

            return response
        else:
            response = jsonify({
                'message': 'all fields are required'
            })

            response.status_code = 401
            return response
    @app.route('/users', methods=['GET'])
    def users():
        users = Users.get_all()
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
            abor(404)
        user.name = str(request.data.get('name', ''))
        user.email = str(request.data.get('email', ''))
        user.role = str(request.data.get('role', ''))

        user.save()
        response = jsonify({
            'id': user.id,
            'name': str(request.data.get('name', '')),
            'msg': 'Update successful'
        })
        response.status_code = 200

        return response



    return app