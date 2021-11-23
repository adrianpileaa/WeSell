from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
	path('login/', views.login_view, name = 'login'),
	path('register/', views.register_view, name = 'register'),
	path('after_register/<profile_id>/',views.after_register_view, name='after-register'),
	path('logout/', views.logout_view, name = 'logout'),
	path('account/<profile_id>', views.account_view, name = 'account')
]