from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm, LoginForm
from django.contrib.auth.decorators import login_required


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request,user)
            messages.success(request, ('You are now registered'))
            return redirect('home')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context) 


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request,('Youre logged in'))
                return redirect('home')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required
def logout_user(request):
    logout(request)
    messages.success(request,('Youre now logged out'))
    return redirect('home')


@login_required
def edit_profile(request):
    if request.method =='POST':
        form = EditProfileForm(request.POST, instance= request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('You have edited your profile'))
            return redirect('edit_profile')
    else: 		
        form = EditProfileForm(instance= request.user) 

    context = {'form': form}
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else: 		
		form = PasswordChangeForm(user= request.user) 

	context = {'form': form}
	return render(request, 'accounts/change_password.html', context)
