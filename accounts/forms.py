from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class EditProfileForm(UserChangeForm):
	password = forms.CharField(label="", widget=forms.TextInput(attrs={'type':'hidden'}))
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email','password',)
		  



class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2',)