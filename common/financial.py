from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime

from common.query import Query
from common.payment import Payment
import json

class Financial(Resource):
    def get(self):

        try:

            employee_id = request.args.get("employee_id", None)
            start_date = request.args.get("start_date", None)
            end_date = request.args.get("end_date", None)

            if employee_id is None:
                return "Employee ID is missing", 400
            
            if start_date is None and end_date is not None:
                return "Must provide a starting date", 400
            
            if start_date is None and end_date is None:
                payment = Payment()
                payments = payment.get_employee_payments(employee_id)
            else:

                if start_date is not None and end_date is None:
                    end_date = datetime.now()

                payment = Payment()
                all_payments = payment.get_employee_payments(employee_id)
                payments = payment.get_payments_between_dates(all_payments, start_date, end_date)
            
            return json.dumps(payments)
        except Exception as error:
            print (error)
            return "An unexpected error occured", 500
