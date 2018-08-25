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
from .views import (PasswordChangeView,
                    PasswordResetView,
                    LoginView,
                    LogoutView
                    )


app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='index'),
    # override login
    path('login', LoginView.as_view(), name='login'),
    # override logout
    path('logout', LogoutView.as_view(), name='logout'),
	# view for registering new profile/acct
	path('register', views.register, name='register'),
	# view for user to modify their profile
	path('edit', views.edit, name='edit'),
    # view for user to change their password
    path('change_password', PasswordChangeView.as_view(), name='change_password'),
    # user is sent here by PasswordChangeView
    path('password_change_done', views.password_change_done, name='password_change_done'),
     # user forgot password
    path('password_reset', PasswordResetView.as_view(), name='password_reset'),
     # user provided email for reset, is sent here by PasswordResetView
    path('password_reset_done', views.password_reset_done, name='password_reset_done'),
]