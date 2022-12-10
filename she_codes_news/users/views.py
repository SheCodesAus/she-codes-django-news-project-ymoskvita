from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import generic

from .models import CustomUser
from .forms import CustomUserCreationForm

# Create your views here.


class CreateAccountView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/createAccount.html'

class AccountView(generic.DetailView):
    model = CustomUser
    template_name = 'users/account.html'
    context_object_name = 'user'