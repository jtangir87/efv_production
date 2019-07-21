from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .forms import CreateUserForm, UserSignUpForm, UpdateUserForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.

class SignUp(CreateView):
    form_class = UserSignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
            c = {'form': form, }
            user = form.save(commit=False)
            # Cleaned(normalized) data
            phone_number = form.cleaned_data['phone_number']

            user.save()
    
            # Create UserProfile model
            UserProfile.objects.create(user=user, phone_number=phone_number)
    
            return super(SignUp, self).form_valid(form) 

class UserList(ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        user_list = User.objects.filter(is_superuser=False).order_by('last_name')
        return user_list

class CreateUser(CreateView):
    form_class = CreateUserForm
    template_name = 'accounts/user_form.html'
    success_url = '/accounts/users/'

    def form_valid(self, form):
            c = {'form': form, }
            user = form.save(commit=False)
            # Cleaned(normalized) data
            phone_number = form.cleaned_data['phone_number']

            user.save()
    
            # Create UserProfile model
            UserProfile.objects.create(user=user, phone_number=phone_number)
    
            return super(CreateUser, self).form_valid(form)



# class CreateUser(CreateView):
#     model = User
#     fields = ['username', 'first_name', 'last_name', 'email', 'is_staff']
#     template_name = 'accounts/user_form.html'
#     success_url = '/accounts/users/'

class UpdateUser(UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'accounts/update_user_form.html'
    success_url = '/accounts/users/'

    def form_valid(self, form):
            c = {'form': form, }
            user = form.save(commit=False)
            # Cleaned(normalized) data
            phone_number = form.cleaned_data['phone_number']

            user.save()
    
            # Create UserProfile model
            UserProfile.objects.update(user=user, phone_number=phone_number)
    
            return super(UpdateUser, self).form_valid(form)

   
class UserDetail(DetailView):
    model = User
    template_name='accounts/user_detail.html'

    
    
    
