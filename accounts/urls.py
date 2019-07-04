"""accounts URL Configuration

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
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUp, UserList, CreateUser, UserDetail, UpdateUser


app_name = 'accounts'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',SignUp.as_view(),name='signup'),
    path('users/',UserList.as_view(),name='user_list'),
    path('users/add/',CreateUser.as_view(),name='create_user'),
    path('profile/<int:pk>/',UserDetail.as_view(),name='user_detail'),
    path('profile/update/<int:pk>/',UpdateUser.as_view(),name='update_user'),
    # path('profile/update/password/',auth_views.PasswordChangeView.as_view
    #     (template_name='registration/password_change_form.html'),name='password_change'),
    path('password/reset/',auth_views.PasswordResetView.as_view
        (template_name='registration/password_reset_form.html'),name='password_reset'),
    path('password/reset/done/',auth_views.PasswordResetDoneView.as_view
        (template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('password/reset/<uid64>/<token>/',auth_views.PasswordResetConfirmView.as_view
        (template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'), 
    path('password_reset/complete/',auth_views.PasswordResetCompleteView.as_view
        (template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('password/change/',auth_views.PasswordChangeView.as_view
        (template_name='registration/password_change_form.html'),name='password_change'),
    path('password/change/done/',auth_views.PasswordChangeDoneView.as_view
        (template_name='registration/password_change_done.html'),name='password_change_done'),

]
