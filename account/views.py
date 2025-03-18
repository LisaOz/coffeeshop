from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login
# Create your views here.


def user_login(request):
    # if the user submits the form with the POST request, the form is instantiated with the submitted data
    # with the LoginForm(request.POST), then validated with form.is_valid(). If invalid, the error message is displayed

    if request.method == 'POST':
        form = LoginForm(request.POST)

        # If the form is validated, the user is authenticated against the database with authenticate() method
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                # if the used is active, it is logged into the site and set into the session with login() method
                if user.is_active:
                    login(request, user)
                    return HttpResponse('User authenticated successfully')  # returns the user object
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})



def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('shop:product_list')  # Redirect to shop or another page
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})