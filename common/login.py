from flask_restful import Resource, reqparse
from flask import request, jsonify

from common.globals import JWT_SECRET_KEY
from functools import wraps

from common.query import Query
from common.payment import Payment
import json

import jwt

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

def validate_credentials():
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header or "Bearer" not in auth_header:
            return "Bad authorization header", 403

        auth_header_data = auth_header.split(" ")
        if not len(auth_header_data) == 2:
            return "Bad authorization header", 401

        query = Query('authentication')

        _, token = auth_header_data

        decoded_data = jwt.decode(token, JWT_SECRET_KEY)

        username = decoded_data.get('username')
        password = decoded_data.get('password')

        user = query.select().where(username=username, password=password).get()
        
        if len(user) == 0:
            return "User was not found", 404

    except Exception:
        return "Token is invalid", 403

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        validated = validate_credentials()

        if validated is not None:
            return validated

        return f(*args, **kwargs)
    return decorated

def get_jwt_token(credentials):
    return jwt.encode(credentials, JWT_SECRET_KEY).decode('UTF-8')

class Login(Resource):
    
    def post(self):
        try:

            login_payload = parser.parse_args()

            username = login_payload.get('username', None)
            password = login_payload.get('password', None)
            
            if username is None:
                return "No username was provided", 401
                
            query = Query("authentication")
            
            user = query.select().where(username=username)
            user_data = user.get()[0]

            if user_data['is_locked'] == "Y":
                return "Account is locked", 403

            if user_data['password'] != password:
                attempts = int(user_data['failed_attempts']) + 1
                
                if attempts == 3:
                    user.update(is_locked="Y", failed_attempts=str(attempts))
                else:
                    user.update(failed_attempts=str(attempts))
            
                return "Incorrect username/password combination", 401
            return json.dumps({
                "token": get_jwt_token({'username': username, 'password': password}),
                "username": username}), 200
        except Exception as error:
            return error, 500
