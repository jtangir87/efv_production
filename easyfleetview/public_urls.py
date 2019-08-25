"""easyfleetview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from .views import SignUpComplete
from . import views

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', views.trialsignup, name='public'),
    path('submitted', SignUpComplete.as_view(), name='signup_complete'),
    path('stripe/webhook', views.stripe_webhooks, name='stripe_webhook'),

]
