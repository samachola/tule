import os
import datetime
import jwt
from json.decoder import JSONDecodeError
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from flask import Blueprint, request, jsonify, make_response, json, url_for
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from app import app, models
from app.models import Users, Location, Restaurant, Category

partner = Blueprint('restaurant', __name__)

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


@partner.route('', methods=['POST'])
@token_required
def new_restaurant(current_user):
    """
    Method for adding a new restaurant
    """
    if current_user.role != 'admin':
        response = jsonify({
            'message': 'Unauthorized command',
            'status': False
        })
        response.status_code = 401

        return response
    
    data = request.get_json()

    restaurant_name = str(data['restaurant_name'])
    restaurant_email = str(data['restaurant_email'])
    restaurant_county = str(data['restaurant_county'])
    restaurant_location = str(data['restaurant_location'])
    restaurant_minorder = str(data['restaurant_minorder'])
    restaurant_phone = str(data['restaurant_phone'])
    restaurant_mobile = str(data['restaurant_mobile'])
    restaurant_about = str(data['restaurant_about'])
    restaurant_delivery = str(data['restaurant_delivery'])

    if restaurant_name.isspace() or restaurant_email.isspace() or restaurant_county.isspace() or restaurant_location.isspace():
        response = jsonify({
            'message': 'All fields are required',
            'status': False
        })

        return response
    elif restaurant_minorder.isspace() or restaurant_phone.isspace() or restaurant_mobile.isspace():
        reponse = jsonify({
            'message': 'All fields are required',
            'status': False
        })

        return response
    elif restaurant_about.isspace() or restaurant_delivery.isspace():
        response = jsonify({
            'message': 'All fields are required',
            'status': False
        })

        response.status_code = 403
        return response
    else: 
        new_restaurant = Restaurant(restaurant_name, restaurant_email, restaurant_county, restaurant_location, restaurant_minorder, restaurant_phone, restaurant_mobile, restaurant_about, restaurant_delivery)
        new_restaurant.save()

        response = jsonify({
            'Message': 'Successfully added new Restaurant',
            'Status': True
        })

        response.status_code = 201
        return response

@partner.route('', methods=['GET'])
def get_restaurants():
    """
    Gets the list of all restaurants
    """

    restaurants = []

    all_restaurants = Restaurant.query.all()
    for restaurant in all_restaurants:
        rest = {
            'id': restaurant.id,
            'restaurant_name': restaurant.restaurant_name,
            'restaurant_email': restaurant.restaurant_email,
            'restaurant_county': restaurant.restaurant_county,
            'restaurant_location': restaurant.restaurant_email,
            'restaurant_minorder': restaurant.restaurant_minorder
        }

        restaurants.append(rest)

    response = jsonify({
        'status': True,
        'restaurants': restaurants
    })

    response.status_code = 200
    return response
      

@partner.route('/category', methods=['POST'])
@token_required
def add_category(current_user):
    if current_user.role != 'admin':
        response = jsonify({
            'message': 'You don\'t have the right permission',
            'status': False
        })
        response.status_code = 403
        return response

    data = request.get_json()
    new_category = Category(data['restaurant_id'], data['category_name'])
    new_category.save()

    response = jsonify({
        'message': 'Successfully added new category',
        'status': True
    })

    response.status_code = 201
    return response

@partner.route('/categories/<int:id>', methods=['GET'])
@token_required
def get_categories(current_user, id):
    """Gets the list of categories by restaurant_id."""
    categories = []

    cats = Category.query.filter_by(restaurant_id=id).all()
    for cat in cats:
        category = {
            'id': cat.id,
            'name': cat.name,
            'restaurant': cat.restaurant_id
        }
        categories.append(category)

    response = jsonify({
        'status': True,
        'categories': categories
    })

    response.status_code = 200
    return response

@partner.route('/category/<int:id>', methods=['PUT'])
@token_required
def edit_category(current_user, id):
    """Edits the restaurants menu category."""
    data = request.get_json()
    restaurant_category = Category.query.filter_by(id=id).first()
    if not restaurant_category:
        return jsonify({'message': 'Category not found', 'status': False})
    restaurant_category.name = str(data['category_name'])
    db.session.commit()

@partner.route('/category/<int:id>', methods=['DELETE'])
@token_required
def delete_category(current_user, id):
    """Deletes the category by id."""
    restaurant_category = Category.query.filter_by(id=id).first()
    if not restaurant_category:
        return jsonify({'message': 'category not found', 'status': False})
    db.session.delete(restaurant_category)
    db.session.commit()

    return jsonify({'message': 'Category has been successfully deleted', 'status': True})