"""eticketing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.shortcuts import redirect
import new.views as v

urlpatterns = [
    path('', lambda request: redirect('accounts/login')),
    path('accounts/', include("django.contrib.auth.urls")),
    path('home', v.home, name='home'),
    path('flight', v.flight, name='flight'),
    path('contact', v.contact, name='contact'),
    path('signup', v.signup, name='signup'),
    path('admin/', admin.site.urls, name='admin'),
    path('booking/<int:pk>/', v.book, name='book'),
    path('manage_booking', v.manage_booking, name='manage_booking'),
    # path('search-flight', v.searchFlight, name='search-flight')
    
]
