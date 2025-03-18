from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm

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
