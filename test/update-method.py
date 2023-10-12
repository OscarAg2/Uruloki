import unittest
from unittest.mock import MagicMock,patch
from index import app, update_customer

class TestUpdateCustomer(unittest.TestCase):
    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()
        
        # Mock the MongoDB collection object
        self.collection = MagicMock()
        self.collection.find_one.return_value = {'_id': '123', 'codigo-cliente': 'CLI12345'}
        self.collection.update_one.return_value.modified_count = 1
        
        # Patch the MongoDB collection object in the function
        self.patcher = patch('index.db.get_collection')
        self.mock_get_collection = self.patcher.start()
        self.mock_get_collection.return_value = self.collection
        
    def tearDown(self):
        # Stop patching the MongoDB collection object
        self.patcher.stop()
        
    def test_update_customer_success(self):
        # Make a PUT request to the update endpoint with test data
        response = self.app.put('/update?credito=1000&nombre_completo=Juan,Perez&codigo=CLI12345')
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the response message is correct
        self.assertEqual(response.data.decode('utf-8'), 'Customer information updated successfully')
        
        # Check that the collection object was called with the correct arguments
        self.collection.find_one.assert_called_once_with({'codigo-cliente': 'CLI12345'})
        self.collection.update_one.assert_called_once_with({'codigo-cliente': 'CLI12345'}, {'$set': {'nombre-completo': ['Juan', 'Perez'], 'credito': '1000'}})
        
    def test_update_customer_not_found(self):
        # Mock the MongoDB collection object to return None
        self.collection.find_one.return_value = None
        
        # Make a PUT request to the update endpoint with test data
        response = self.app.put('/update?credito=1000&nombre_completo=Juan,Perez&codigo=CLI12345')
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the response message is correct
        self.assertEqual(response.data.decode('utf-8'), 'Customer not found')
        
        # Check that the collection object was called with the correct arguments
        self.collection.find_one.assert_called_once_with({'codigo-cliente': 'CLI12345'})
        self.collection.update_one.assert_not_called()