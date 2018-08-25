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

app_name = 'cemex'

urlpatterns = [
    # index (currently redirects to login or my orders)
    path('', views.index, name='index'),
    # new order (lists items in order forms)
	path('new_order', views.new_order, name='new_order'),
    # confirm order (review/delete items in incomplete order)
	path('confirm_order', views.confirm_order, name='confirm_order'),
    # place order (marks incomplete order as complete, sends itemizations email)
	path('place_order/', views.place_order, name='place_order'),
    # my orders (shows orders user has placed)
	path('my_orders', views.my_orders, name='my_orders'),
    # links on my orders view takes user here. itemizated view of a submitted order.
    path('review_order/<order_id>/', views.review_order, name='review_order'),
    # accepts an order uuid and marks the order shipped/processed for user's knowledge (INCOMPLETE)
    #path('process_order/<order_uuid>/', views.process_order, name='review_order'),
	
]
