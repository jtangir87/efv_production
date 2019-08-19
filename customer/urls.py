"""fuellog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path
from customer.views import (
    TenantDetail, billing_new, cancel_subscription, SubscriptionCancelSuccess, 
    SubscriptionSuccess, SubscriptionCancelConfirm, BillingProfileTest
)

app_name = 'client'

urlpatterns = [
    path('', TenantDetail.as_view(), name='client_details'),
    path('billing/', billing_new, name='billing_profile'),
    path('subscribe/', BillingProfileTest.as_view(), name='subscribe'),
    path('billing/cancel/success', cancel_subscription, name='cancel_subscription'),
    path('billing/cancel/', SubscriptionCancelConfirm.as_view(), name='subscription_cancel_confirm'), 
    path('subscribe/success', SubscriptionSuccess.as_view(), name='subscription_success'),

]