from django.test import TestCase
from django.urls import reverse
from accounts.models import User


class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.logout_url=reverse('logout')
        self.edit_profile_url=reverse('edit_profile')
        self.change_password_url=reverse('change_password')
        self.user={
            'email':'testemail@gmail.com',
            'password1':'hfhfhhf64646',
            'password2':'hfhfhhf64646',
        }
        self.user_short_password={
            'email':'testemail@gmail.com',
            'password1':'tes',
            'password2':'tes',
        }
        self.user_unmatching_password={
            'email':'testemail@gmail.com',
            'password1':'teslatt',
            'password2':'teslatto',
        }

        self.user_invalid_email={            
            'email':'test.com',
            'password1':'teslatt',
            'password2':'teslatto',
        }
        return super().setUp()

class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response=self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/register.html')

    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

    def test_double_register_redirect_home(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(str(response.url),'/')
        

    def test_cant_register_user_with_short_password(self):
        response=self.client.post(self.register_url,self.user_short_password,format='text/html')
        self.assertEqual(response.status_code,400)

    def test_cant_register_user_with_unmatching_passwords(self):
        response=self.client.post(self.register_url,self.user_unmatching_password,format='text/html')
        self.assertEqual(response.status_code,400)

    def test_cant_register_user_with_invalid_email(self):
        response=self.client.post(self.register_url,self.user_invalid_email,format='text/html')
        self.assertEqual(response.status_code,400)

    def test_cant_register_user_with_taken_email(self):
        self.client.post(self.register_url,self.user,format='text/html')
        self.client.get(self.logout_url)
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,400)

class LoginTest(BaseTest):
    def test_can_access_page(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/login.html')

    def test_double_login_redirect_home(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response= self.client.post(self.login_url,{'email':self.user['email'],'password':self.user['password1']},format='text/html')
        self.assertEqual(str(response.url),'/')

    def test_login_success(self):
        self.client.post(self.register_url,self.user,format='text/html')
        self.client.get(self.logout_url)
        response= self.client.post(self.login_url,{'email':self.user['email'],'password':self.user['password1']},format='text/html')
        self.assertEqual(response.status_code,302)

    def test_cant_login_with_invalid_creds(self):
        response= self.client.post(self.login_url,{'email':'hello@gmail.com','password1':'fghfh154654'},format='text/html')
        self.assertEqual(response.status_code,400)

class ModelTest(BaseTest):
    def test_model_dunder_str(self):
        self.client.post(self.register_url,self.user,format='text/html')
        user = User.objects.get(email=self.user['email'])
        self.assertEqual(str(user), self.user['email'])

class ProfileTest(BaseTest):
    def test_edit_profile_GET(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response = self.client.get(self.edit_profile_url,format='text/html')
        self.assertEqual(response.status_code,200)

    def test_edit_profile_POST(self):
        self.client.post(self.register_url,self.user,format='text/html')
        context = {
            'email': self.user['email'],
            'name': 'testnamechanged',
            'password': self.user['password1'],
        }
        self.client.post(self.edit_profile_url,context,format='text/html')
        user = User.objects.get(name='testnamechanged')
        self.assertEqual(user.name, 'testnamechanged')

    def test_password_change_GET(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response = self.client.get(self.change_password_url,format='text/html')
        self.assertEqual(response.status_code,200)

    def test_password_change_POST_400(self):
        self.client.post(self.register_url,self.user,format='text/html')
        context = {
            'old_password': self.user['password1'],
            'new_password1': 'testpwdadmin345345',
            'new_password2': 'testpwdadmin345345',
        }
        self.client.post(self.change_password_url,context,format='text/html')
        self.client.get(self.logout_url)
        response= self.client.post(self.login_url,{'email':self.user['email'],'password':self.user['password1']},format='text/html')
        self.assertEqual(response.status_code,400)

    def test_password_change_POST_200(self):
        self.client.post(self.register_url,self.user,format='text/html')
        context = {
            'old_password': self.user['password1'],
            'new_password1': 'testpwdadmin345345',
            'new_password2': 'testpwdadmin345345',
        }
        self.client.post(self.change_password_url,context,format='text/html')
        self.client.get(self.logout_url)
        response= self.client.post(self.login_url,{'email':self.user['email'],'password':context['new_password1']},format='text/html')
        self.assertEqual(response.status_code,302)
