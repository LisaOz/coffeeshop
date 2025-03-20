from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from orders.models import Order
from .forms import LoginForm



# Create your views here.


"""
View for user login

"""
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



"""
View for user registration
"""


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():  # if form is valid
            user = form.save() # save the new user
            login(request, user)  # Log the user in after successful registration

            # Check if there's a 'next' URL to redirect the user to
            next_url = request.POST.get('next', 'shop:product_list')  # Default to 'shop:product_list' if no 'next'
            return redirect(next_url)  # Redirect to the next page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



"""
View for dashboard
"""


# the decorator is used to check if the current user is authenticated.
# If the user is not authenticated, it redirects the user to the login URL.
# Login view redirects users tp the URL they were trying to access by using
# hidden <input> HTML element 'next' in Login template



@login_required
def dashboard(request):
    # fetch orders from the Order model where user matches the currently logged-in user
    user_orders = Order.objects.filter(user=request.user)  # Get orders of the logged-in user

    return render(request, 'dashboard.html', {'user_orders': user_orders})  # Pass user_orders variable to the template
