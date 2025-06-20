import tempfile
from functools import wraps

import weasyprint
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from cart.cart import Cart
from django.shortcuts import get_object_or_404, redirect, render
from .forms import OrderCreateForm
from .models import Order, OrderItem
from shop.models import StaffRole
from .tasks import order_created
from weasyprint import HTML, CSS
from django.http import HttpResponse
from django.template.loader import render_to_string

"""
This is a view to generate a PDF invoice for an order
Decorate is used to indicate tht only staff users can access this view.
"""


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Render the HTML template to a string
    html = render_to_string('orders/order/pdf.html', {'order': order})

    # Create an HTTP response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    try:
        # Write the PDF to the HTTP response
        weasyprint.HTML(string=html).write_pdf(
            response,
            stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))]
        )
        return response
    except Exception as e:
        return HttpResponse("Error generating PDF", status=500)


"""
View for the 'order_create' 
"""



def order_create(request):

    cart = Cart(request)  # get the current cart from the session cart
    form = OrderCreateForm()  # to ensure 'form' is always defined
    if request.method == 'POST':  # Validates the data sent in the request
        form = OrderCreateForm(request.POST)
        if form.is_valid():  # create an order and associate it with the logged-in user
            order = form.save(commit=False)

            if not request.user.is_authenticated:
                messages.error(request, "Please, log in to place the order")
                return redirect('account:login')  # Redirect to login page if not authenticated
            order.user = request.user  # Associate the order with the logged-in user
            order.save()  # save the order into the database
            print(f"New order created with status: {order.status}")


            # Create OrderItems for each item in the cart
            for item in cart:  # iterate over all items in the cart and create a new order in the database
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()  # Clear the cart

            # Launch asynchronous task to send the email message (to the console) about the placed order.
            # The delay() method of the task is called to execute it asynchronously. The task will be added
            # to the message queue and executed by the Celery worker

            order_created.delay(order.id)

            # set the order in the session
            request.session['order_id'] = order.id

            # redirect for payment
            return redirect('payment:process')

    else:
        form = OrderCreateForm()

    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )


# Use the decorator to check that both the is_active and is_staff fields of the user requesting the page is set to True
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # get the Order object with the given ID
    return render(
        request, 'admin/orders/order/detail.html', {'order': order}  # render the template to display the order
    )





# Payment successful and order completion page
@login_required
def payment_completed(request):
    # Get the user's orders after payment completion
    user_orders = Order.objects.filter(user=request.user)

    # After successful payment
    return render(request, 'payment/completed.html', {'user_orders': user_orders})




"""
View for barista dashboard
"""


def barista_required(view_func):
    """Decorator to restrict access to baristas only."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('staff_account:staff_login')  # Redirect to staff login
        if not request.user.groups.filter(name='Barista').exists():
            return redirect('shop:home')  # Redirect unauthorized users to home

        return view_func(request, *args, **kwargs)

    return wrapper


def barista_dashboard(request):
    orders = Order.objects.all()  # Fetch all orders
    return render(request, 'barista_dashboard.html', {'orders': orders})




"""
View for order status on the barista dashboard
"""


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.groups.filter(name="barista").exists():

        if request.method == "POST":
            new_status = request.POST.get("status")

            # Ensure new status is valid
            valid_statuses = [Order.PENDING, Order.PREPARING, Order.READY_TO_COLLECT, Order.COLLECTED]
            if new_status in valid_statuses:
                order.status = new_status
                order.save()
                return redirect('barista_dashboard')
            else:
                return HttpResponse("Invalid status", status=400)
    return HttpResponse("Unauthorised", status=403)




@barista_required
def mark_order_preparing(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = "Preparing"
        order.save()
        return redirect('orders:barista_dashboard')
    return render(request, 'orders/mark_order_preparing.html', {'order': order})


@barista_required
def mark_order_ready_co_collect(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = "Ready co Collect"
        order.save()
        return redirect('orders:barista_dashboard')  # Redirect to dashboard
    return render(request, 'orders/mark_order_ready_to_collect.html', {'order': order})



@barista_required
def mark_order_collected(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = "Collected"
        order.save()
        return redirect('orders:barista_dashboard')  # Redirect to dashboard

    return render(request, 'orders/mark_order_collected.html', {'order': order})



