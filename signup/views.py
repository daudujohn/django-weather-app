from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from weatherapp.models import User
from weatherapp.views import index
# from django.contrib.auth.forms import UserCreationForm
from .forms import EmailSignUpForm

import weatherapp.getWeather

# class CustomUserCreationForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
#         self.fields['username'].label = 'Email'
#         self.fields['username'].help_text = ''
#         self.fields['password1'].label = 'Password'
#         self.fields['password1'].help_text = ''
#         self.fields['password2'].label = 'Password'
#         self.fields['password2'].help_text = ''


# Create your views here.
def signup(request):
    print('signnnuppppppp viewwwwwww')
    context = weatherapp.getWeather.getWeather(request)
    if request.method == 'POST':
        form = EmailSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(email, password)
            user.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = EmailSignUpForm()

    context.update({'form': form})
    return render(request, 'signup/signup.html', context)

def login(request):
    print('loginnnnnnnnn')
    return index(request)