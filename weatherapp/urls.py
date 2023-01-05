from django.urls import path
from . import views as weatherapp_views
from signup import views as signup_views

urlpatterns = [
    path('', weatherapp_views.index),
    path('signup/', signup_views.signup, name='signup')
]