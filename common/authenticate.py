from common.query import Query
from common.globals import JWT_SECRET_KEY

from functools import wraps
from flask import request

import jwt


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