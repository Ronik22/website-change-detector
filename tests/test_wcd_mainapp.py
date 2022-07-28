from django.test import TestCase

# Create your tests here.
# TODO

class SimpleTestNoLogin(TestCase):
    
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_tasks_nologin(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 302)
    
    def test_tasks_add_nologin(self):
        response = self.client.get('/tasks/add/')
        self.assertEqual(response.status_code, 302)