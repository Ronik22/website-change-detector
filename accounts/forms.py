from accounts.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.Form):
	email = forms.EmailField(max_length=100)
	password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class EditProfileForm(UserChangeForm):
	password = forms.CharField(label="", widget=forms.TextInput(attrs={'type':'hidden'}))
	class Meta:
		model = User
		fields = ('email','name','password')
		  

class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('email', 'password1', 'password2',)