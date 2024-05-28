from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, LoginForm


def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('authentication:login')

        messages.add_message(request, messages.INFO, form.errors)
        return render(request, 'auth/register.html')

    if request.user.is_authenticated:
        return redirect('projects:index')
    return render(request, 'auth/register.html')


def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))

            if user:
                login(request, user)
                return redirect('projects:index')
            else:
                messages.add_message(request, messages.INFO, 'Пользователь не найден')
        else:
            messages.add_message(request, messages.INFO, form.errors)

        return render(request, 'auth/login.html')

    if request.user.is_authenticated:
        return redirect('projects:index')
    return render(request, 'auth/login.html')


@login_required()
def logoutView(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))
