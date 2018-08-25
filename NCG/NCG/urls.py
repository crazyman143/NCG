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
from django.contrib import admin
from django.urls import include, path


# need this for serving images in debug
from django.conf import settings
from django.conf.urls.static import static

import debug_toolbar


urlpatterns = [
    # redirect root to cemex
    path('', include('cemex.urls', namespace='home')),
	# app for authenticating users
	path('profiles/', include('profiles.urls', namespace='profiles')),
	
	# app for cemex ordering
    path('cemex/', include('cemex.urls', namespace='cemex')),
	
	# built in admin 
	path('admin/', admin.site.urls),
	
	# django debug toolbar
	path(r'^__debug__', include(debug_toolbar.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# these settings are for debug_toolbar only:

from django.conf import settings
from django.conf.urls import include, url

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
	
