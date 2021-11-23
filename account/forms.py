from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from .models import Profile

class RegisterForm(ModelForm):

	class Meta:
		model = User
		fields = ('email', 'username', 'password')


	def clean_email(self):
		email = self.cleaned_data.get('email')
		try:
			account = User.objects.get(email = email)
		except Exception as e:
			return email 
		raise forms.ValidationError(f"Email {email} already exists")
		
	def clean_username(self):
		username = self.cleaned_data.get('username')
		try:
			account = User.objects.get(username = username)
		except Exception as e:
			return username
		raise forms.ValidationError(f"Username {username} already exists")

class AuthenticationForm(forms.ModelForm):

	password = forms.CharField(max_length = 30, widget = forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('username', 'password')
	
	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username = username, password = password)
		if not user:		
			raise forms.ValidationError('Login Invalid')
		return self.cleaned_data

class ChangeProfilePicture(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('profile_picture',)