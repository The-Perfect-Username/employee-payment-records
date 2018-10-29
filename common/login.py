from flask_restful import Resource, reqparse
from flask import request
from common.query import Query
from common.payment import Payment
from common.authenticate import token_required, get_jwt_token
import json

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

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
