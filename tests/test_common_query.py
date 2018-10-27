import unittest
from unittest.mock import MagicMock, patch
from common.query import Query

class TestQuery(unittest.TestCase):
    
    def test_create_new_query_instance_raises_value_error(self):
        with self.assertRaises(ValueError):
            query = Query()
    
    def test_create_new_query_instance_raises_value_error_because_unsupported_entity(self):
        class InvalidEntity:
            pass

        with self.assertRaises(ValueError):
            query = Query(InvalidEntity)
    
    def test_create_new_query_instance_passes(self):
        
        query = Query("authentication")

        self.assertIsInstance(query, Query)
        self.assertEqual(query.entity_name, "authentication")

    def test_fetch_records_reading_file(self):
        query = Query("authentication")

        records = query.fetch_records

        self.assertIsInstance(records, list)
        self.assertIsInstance(records[0], dict)
        self.assertDictEqual(records[0], {
            "username": "MaolinXu",
            "password": "1111s1",
            "is_locked": "N",
            "failed_attempts": "0"
        })
    
    
    def test_select_method(self):
        query = Query("authentication")

        records = query.select()

        self.assertIsInstance(records, Query)
        
        records = records.results
        
        self.assertIsInstance(records, list)
        self.assertIsInstance(records[0], dict)
        self.assertDictEqual(records[0], {
            "username": "MaolinXu",
            "password": "1111s1",
            "is_locked": "N",
            "failed_attempts": "0"
        })
    
    @patch('common.query.Query.get')
    def test_get_method(self, query_mock):
        
        query = Query("authentication")
        query_mock.return_value = []
        
        self.assertListEqual(query.select().get(), [])

        # query = Query("authentication")

        # records = query.select().get()

        # self.assertIsInstance(records, list)
        # self.assertIsInstance(records[0], dict)
        # self.assertDictEqual(records[0], {
        #     "username": "MaolinXu",
        #     "password": "1111s1",
        #     "is_locked": "N",
        #     "failed_attempts": "0"
        # })
    
    def test_selecting_with_conditions_username_only(self):
        query = Query("authentication")

        records = query.select().where(username="Jason").get()

        self.assertIsInstance(records, list)
        self.assertIsInstance(records[0], dict)
        self.assertDictEqual(records[0], {
            "username": "Jason",
            "password": "jhDFdsk",
            "is_locked": "N",
            "failed_attempts": "0"
        })
    
    def test_selecting_with_conditions_returns_nothing_because_of_incorrect_value(self):
        query = Query("authentication")

        records = query.select().where(username="Jason", password="abc").get()

        self.assertIsInstance(records, list)
        self.assertListEqual(records, [])
    
    def test_selecting_with_multiple_conditions(self):
        query = Query("authentication")

        records = query.select().where(username="Annabelle55", password="123EDCDE4", is_locked="Y").get()

        self.assertIsInstance(records, list)
        self.assertDictEqual(records[0], {
            "username": "Annabelle55",
            "password": "123EDCDE4",
            "is_locked": "Y",
            "failed_attempts": "0"
        })



if __name__ == '__main__':
    unittest.main()