import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity as identity_function
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # can change to MySQL, PostgreSQL etc
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'eugene'
api = Api(app)

# change jwt authentication url, have to before jwt = JWT(...)
# app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity_function) # create an endpoint: /auth

# customize JWT auth response, include user_id in response body
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1/item/macbook
api.add_resource(Store, '/store/<string:name>')  # http://127.0.0.1/item/macbook
api.add_resource(ItemList, '/items')  # http://127.0.0.1/items
api.add_resource(StoreList, '/stores')  # http://127.0.0.1/items

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    # Only import here, because prevent circular import
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
