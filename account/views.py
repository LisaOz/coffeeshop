from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.core.checks import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from coffeeshop import settings
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
                    return redirect('account:dashboard')
                    #return HttpResponse('User authenticated successfully')  # returns the user object
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



# View to see account details and change the password
@login_required
def account_details(request):
    if request.method == 'POST':
        # Handle password change
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if password_form.is_valid():
            password_form.save()
            messages.success(request, "Password changed successfully!")
            return redirect('account:dashboard')  # Redirect to prevent re-submission
    else:
        password_form = PasswordChangeForm(user=request.user)

    # Render the page with both the user info and the password form
    return render(request, 'registration/account_details.html', {'user': request.user, 'password_form': password_form})



"""
View for staff login (role = 'Barista')
"""


def staff_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.groups.filter(name="Barista").exists():  # Check if user is a barista
                login(request, user)
                return redirect(settings.STAFF_LOGIN_REDIRECT_URL)  # Redirect to barista dashboard
            else:
                return redirect('shop:home')  # Redirect unauthorized users to home
    else:
        form = AuthenticationForm()
    return render(request, 'staff_account/staff_login.html', {'form': form})


"""
View for staff logout
"""

def staff_logout(request):
    logout(request)
    return redirect(settings.STAFF_LOGOUT_REDIRECT_URL)  # Redirect to staff login after logout

"""
Barista dashboard_view
"""
@login_required
def barista_dashboard(request):
    if not request.user.groups.filter(name="Barista").exists():
        messages.error(request, "You are not authorized to access this page.")
        return redirect('shop:home')

    orders = Order.objects.filter(status__in=["paid", "pending"]).order_by("created")

<<<<<<< HEAD
    print(orders)  # Debugging to check if orders are being fetched correctly

=======
>>>>>>> a4334d432523e81d4e867f41ae574e4a96ec2fa9
    return render(request, 'staff_account/barista_dashboard.html', {'orders': orders})
