from common.payment import Payment

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

class TestPayment(unittest.TestCase):

    def test_get_all_employee_payments_by_id(self):
        payment = Payment()
        payments = payment.get_employee_payments("1")

        self.assertIsInstance(payments, list)
        self.assertIsInstance(payments[0], dict)
        self.assertDictEqual(payments[0], {
            "employee_id": "1",
            "date": "2014-07-06",
            "gross": "135.25",
            "tax": "24.23"
        })
        
        self.assertDictEqual(payments[-1], {
            "employee_id": "1",
            "date": "2018-07-15",
            "gross": "110.00",
            "tax": "75.10"
        })

    def test_date_str_to_datetime(self):

        payment = Payment()
        converted = payment.date_str_to_datetime("2012-10-31")
        self.assertEqual(datetime(2012, 10, 31), converted)
        self.assertNotEqual(datetime(2012, 10, 30), converted)

    def test_sum_of_all_payments_and_tax(self):
        payment = Payment()

        test_records = [
            {
                "gross": "110.00",
                "tax": "11.00"
            },
            {
                "gross": "220.00",
                "tax": "22.00"
            },
            {
                "gross": "50.00",
                "tax": "5.00"
            }
        ]

        sum_of_gross_and_tax = payment.sum_of_payments_and_tax(test_records)

        self.assertIsInstance(sum_of_gross_and_tax, tuple)
        self.assertEqual(len(sum_of_gross_and_tax), 2)
        self.assertTupleEqual(sum_of_gross_and_tax, (380.00, 38.00))

    def test_get_payments_between_two_dates(self):
        payment = Payment()
        employee_payments = payment.get_employee_payments("1")
        filtered_payments = payment.get_payments_between_dates(employee_payments, "2014-08-10", "2017-07-16")

        self.assertIsInstance(filtered_payments, list)
        self.assertEqual(len(filtered_payments), 154)
        self.assertEqual(filtered_payments[0]['date'], "2014-08-10")
        self.assertEqual(filtered_payments[-1]['date'], "2017-07-16")

    def test_financial_year_date_string(self):

        payment = Payment()
        financial_year = payment.financial_year_date("2014-07-01", "2015-06-30")

        self.assertEqual(financial_year, "2014-2015")
    
    def test_financial_year_date_datetime(self):

        payment = Payment()
        financial_year = payment.financial_year_date(datetime(2014, 7, 1), datetime(2015, 6, 30))

        self.assertEqual(financial_year, "2014-2015")

    def test_compress_financial_records(self):

        payment = Payment()

        employee_payments = payment.get_employee_payments("1")
        latest_financial_year = payment.get_payments_between_dates(employee_payments, "2017-07-01", "2018-06-30")
        condensed_report = payment.compress_financial_year_records(latest_financial_year)
        condensed_report = payment.compress_financial_year_records(latest_financial_year)

        self.assertIsInstance(condensed_report, dict)
        self.assertEqual(condensed_report['financial_year'], "2017-2018")

    def test_separate_payments_by_financial_year(self):
        payment = Payment()

        employee_payments = payment.get_employee_payments("1")
        payments_by_financial_years = payment.separate_payments_by_financial_year(employee_payments)

        self.assertIsInstance(payments_by_financial_years, list)
        self.assertIsInstance(payments_by_financial_years[0], list)
        self.assertEqual(len(payments_by_financial_years), 4)
        self.assertEqual(payments_by_financial_years[0][0]['date'], "2014-07-06")
        self.assertEqual(payments_by_financial_years[0][-1]['date'], "2015-06-28")
        self.assertEqual(payments_by_financial_years[1][0]['date'], "2015-07-05")
        self.assertEqual(payments_by_financial_years[1][-1]['date'], "2016-06-26")

    def test_get_employee_reports(self):

        payment = Payment()
        employee_report = payment.get_employee_reports("1")

        self.assertEqual(len(employee_report), 4)
        self.assertIsInstance(employee_report, list)
        self.assertIsInstance(employee_report[0], dict)
        self.assertEqual(employee_report[0]["financial_year"], "2014-2015")
        self.assertEqual(employee_report[1]["financial_year"], "2015-2016")
        self.assertEqual(employee_report[-1]["financial_year"], "2017-2018")
        

if __name__ == '__main__':
    unittest.main()