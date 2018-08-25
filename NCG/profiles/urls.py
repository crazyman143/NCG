"""Automation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views


app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='index'),
    # handle built-in authentication mechanisms (login, logout, password_change, password_reset)
    path('auth/', include('django.contrib.auth.urls')),
	# view for registering new profile/acct
	path('register', views.register, name='register'),
	# view for user to modify their profile
	path('edit', views.edit, name='edit'),
    # view for user to change their password
    path('change_password', views.change_password, name='change_password'),
]