from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .forms import CreateUserForm, UserSignUpForm, UpdateUserForm, UpdateCurrentUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.

class SignUp(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'


class UserList(ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 25

    def get_queryset(self):
        user_list = User.objects.filter(is_superuser=False).order_by('last_name')
        return user_list

class CreateUser(CreateView):
    form_class = CreateUserForm
    template_name = 'accounts/user_form.html'
    success_url = '/accounts/users/'



class UpdateUser(UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'accounts/update_user_form.html'
    success_url = '/accounts/users/'

class UserDetail(DetailView):
    model = User
    template_name='accounts/user_detail.html'

    
class CurrentUserDetail(DetailView):
    model = User
    template_name='accounts/current_user_detail.html'

    def get_object(self):
        return self.request.user

class UpdateCurrentUser(UpdateView):
    model = User
    form_class = UpdateCurrentUserForm
    template_name = 'accounts/update_current_user_form.html'
    success_url = '/accounts/users/current'

    def get_object(self):
        return self.request.user


    
