import unittest
import requests

class TestAPI(unittest.TestCase):
    def setUp(self):
        # Replace this with your API base URL
        self.base_url = 'http://127.0.0.1:8080'

    def test_get_all_resource(self):
        response = requests.get(f'{self.base_url}/api/all_resource/')
        # print(response.text)
        self.assertEqual(response.status_code, 200)

    def test_get_resource_by_vendor_id(self):
        vendor_id = "104138"  # Replace with a valid resource ID
        response = requests.get(f'{self.base_url}/api/resource/vendor/{vendor_id}')
        # print(response.text)
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data as needed


    def test_get_resource_by_id(self):
        resource_id = 30006385  # Replace with a valid resource ID
        response = requests.get(f'{self.base_url}/api/resource/{resource_id}')
        # print(response.text)
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response data as needed

if __name__ == '__main__':
    unittest.main()