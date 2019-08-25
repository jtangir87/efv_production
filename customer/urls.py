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
    SubscriptionSuccess, SubscriptionCancelConfirm, card_update, reactivate_account,
    reactivate_expired_subscription,
)

app_name = 'client'

urlpatterns = [
    path('', TenantDetail.as_view(), name='client_details'),
    path('subscribe/', billing_new, name='subscribe'),
    path('billing/update-card', card_update, name='card_update'),
    path('subscription/cancel/success', cancel_subscription, name='cancel_subscription'),
    path('subscription/cancel/', SubscriptionCancelConfirm.as_view(), name='subscription_cancel_confirm'), 
    path('subscription/reactivate/', reactivate_account, name='reactivate_account'), 
    path('subscription/expired/reactivate', reactivate_expired_subscription, name='reactivate_expired'),
    path('subscribe/success', SubscriptionSuccess.as_view(), name='subscription_success'),

]