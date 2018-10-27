from common.query import Query
from datetime import datetime

class Payment:

    # Returns all payments for a single employee
    def get_employee_payments(self, employee_id):

        query = Query("pays")
        payment_records = query.select().where(employee_id=employee_id).get()

        return payment_records

    # Returns all employee payments made for each financial year
    def get_employee_reports(self, employee_id):

        query = Query("pays")
        payment_records = query.select().where(employee_id=employee_id).get()

        financial_year_payments = self.separate_payments_by_financial_year(payment_records)

        return [self.compress_financial_year_records(year) for year in financial_year_payments]

    # Separates all payments by financial year
    def separate_payments_by_financial_year(self, payment_records):

        first_date_in_record = self.date_str_to_datetime(payment_records[0]['date'])        
        following_year = first_date_in_record.year + 1
        end_of_financial_year = self.date_str_to_datetime("{}-06-30".format(following_year))
        
        current_financial_year_list = []
        all_financial_years = []

        for payment in payment_records:
            
            date = self.date_str_to_datetime(payment['date'])
            
            if date <= end_of_financial_year:
                current_financial_year_list.append(payment)
            else: 
                following_year = date.year + 1
                end_of_financial_year = self.date_str_to_datetime("{}-06-30".format(following_year))
                
                all_financial_years.append(current_financial_year_list)
                current_financial_year_list = [payment]
        
        return all_financial_years

    def get_payments_between_dates(self, records, start_date, end_date):

        if type(start_date) is str:
            start_date = self.date_str_to_datetime(start_date)
        
        if type(end_date) is str:
            end_date = self.date_str_to_datetime(end_date)

        results = []

        for record in records:
            current_date = self.date_str_to_datetime(record["date"]) 
            if current_date >= start_date and current_date <= end_date:
                results.append(record)

        return results
        

    def compress_financial_year_records(self, financial_year=[]):
        
        if financial_year == []:
            return {}
        
        start_date = financial_year[0]["date"]
        end_date = financial_year[-1]["date"]

        financial_year_date = self.financial_year_date(start_date, end_date)

        sum_of_gross, sum_of_tax = self.sum_of_payments_and_tax(financial_year)

        net_pay = sum_of_gross - sum_of_tax

        return {
            "date": financial_year_date,
            "gross": sum_of_gross,
            "tax": sum_of_tax,
            "net": net_pay
        }

    def financial_year_date(self, start_date, end_date):

        if type(start_date) is str:
            start_date = self.date_str_to_datetime(start_date)
        
        if type(end_date) is str:
            end_date = self.date_str_to_datetime(end_date)

        if start_date.year == end_date.year:
            return "{}-{}".format(start_date.year, end_date.year + 1)
        else:
            return "{}-{}".format(start_date.year, end_date.year)

    def sum_of_payments_and_tax(self, records):
        
        gross = 0.0
        tax = 0.0
        
        for record in records:
            gross += float(record['gross'])
            tax += float(record['tax'])

        return (gross, tax)

    def date_str_to_datetime(self, date_string):
        return datetime.strptime(date_string,'%Y-%m-%d')


        




