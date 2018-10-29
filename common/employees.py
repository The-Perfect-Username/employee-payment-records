from flask_restful import Resource
from common.authenticate import token_required

from common.query import Query
from common.payment import Payment
import json

class Employees(Resource):
    @token_required
    def get(self, employee_id=None):

        if employee_id is None:
            query = Query("employees")
            employees = query.select().get()
            return json.dumps(employees)

        payment = Payment()
        payments = payment.get_employee_reports(employee_id)
        return json.dumps(payments)
