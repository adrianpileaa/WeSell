from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, AuthenticationForm, ChangeProfilePicture
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from products.models import *

def after_register_view(request, **kwargs):
	context = {}
	profile_id = kwargs.get('profile_id')
	profile = Profile.objects.get(id = profile_id)
	
	if request.POST:
		profile.phone_number= request.POST['phone_number']
		profile.first_name = request.POST['first_name'].title()
		profile.last_name = request.POST['last_name'].title()
		profile.save()
		messages.success(request, 'Accounted created succesfully!')
		return redirect('products:home')
	context['profile'] = profile
	return render(request, 'account/after_register.html', context)

def register_view(request):
	context = {}
	if request.user.is_authenticated:
		return HttpResponse('You are already authenticated')
	form = RegisterForm()
	if request.POST:
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False)
			user.set_password(form.cleaned_data['password'])
			user.save()
			username = request.POST['username']
			raw_password = request.POST['password']
			account = authenticate(username = username, password = raw_password)
			if account is not None:
				login(request, account)
				return redirect('account:after-register', profile_id=request.user.id)
		context['register_form'] = form
	else:
		form = RegisterForm()
		context['register_form'] = form

	return render(request, 'account/register.html', context)

def login_view(request):
	if request.user.is_authenticated:
		return redirect('products:home')
	form = AuthenticationForm()
	if request.POST:
		form = AuthenticationForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			raw_password = request.POST['password']
			account = authenticate(username = username, password = raw_password)
			if account:
				login(request, account)
				messages.success(request, 'Login Succesfull!')
				return redirect('products:home')
	else:
		form = AuthenticationForm()
	return render(request, 'account/login.html', {'login_form' : form})

def logout_view(request):
	logout(request)
	return redirect('account:login')

def account_view(request, profile_id):
	context = {}
	account = Profile.objects.get(id = profile_id)
	products = Product.objects.filter(seller_id=profile_id)
	if request.POST:
		image = request.FILES.get('image-changing', '')
		if image:
			account.profile_picture = image
			account.save()
			return redirect('account:account', profile_id = profile_id)
	context['account'] = account
	context['products'] = products
	context['req_id'] = request.user.id
	print(products)
	return render(request, 'account/account.html', context)
