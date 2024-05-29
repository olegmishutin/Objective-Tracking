from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'users'
urlpatterns = [
    path('profile/', login_required(views.ProfileView.as_view()), name='profile')
]
