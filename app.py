from flask import Flask
from flask_restful import Resource, Api

from flask_cors import CORS
from datetime import datetime
from common.query import Query
from common.payment import Payment
import json

from common.login import Login
from common.employees import Employees
from common.financial import Financial

app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

api.add_resource(Login, '/login')
api.add_resource(Employees, '/employees', '/employees/<string:employee_id>')
api.add_resource(Financial, '/payments')

if __name__ == '__main__':
   app.run(debug=True)