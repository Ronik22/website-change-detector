from django.test import TestCase

# Create your tests here.

class SimpleTest(TestCase):
    
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)