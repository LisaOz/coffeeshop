from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from cart.cart import Cart
from django.shortcuts import get_object_or_404, redirect, render
from .forms import OrderCreateForm
from .models import Order, OrderItem
from shop.models import StaffRole
from .tasks import order_created
import weasyprint
from django.http import HttpResponse
from django.template.loader import render_to_string


"""
This is a view to generate a PDF invoice for an order
Decorate is used to indicate tht only staff users can access this view.
"""

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # get the order object with the given ID

    # use Django's render to string function to render a response, rendered HTML response is saved into a variable
    html = render_to_string('orders/order/pdf.html', {'order': order})

    # Generate a new HttpResponse obj specifying the content type and including
    # the Content-Disposition header to specify the file name
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    # use WeasyPrint to generate a PDF file from the rendered HTML code and write to the HTTP response object
    # use css static file to generate an invoice
    # weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))])
    # Correctly generate the PDF using WeasyPrint
    weasyprint.HTML(string=html).write_pdf(  # Generate the PDF
        response,
        stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))]
    )

    # to locate the file you use the finder function of the staticfile module. Return generated response
    return response


"""
View for the 'order_create' 
"""


def order_create(request):
    cart = Cart(request)  # get the current cart from the session cart
    form = OrderCreateForm() # to ensure 'form' is always defined
    if request.method == 'POST': # Validates the data sent in the request
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:  # iterate over all items in the cart and create a new order in the database
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )


            cart.clear() # Clear the cart

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

def barista_required(view_func):
    """Custom decorator to restrict access to baristas only."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if not logged in
        if not StaffRole.objects.filter(user=request.user, name='Barista').exists():
            return redirect('shop:product_list')  # Redirect unauthorized users
        return view_func(request, *args, **kwargs)
    return wrapper


"""Dashboard for baristas to manage orders in preparation"""
@barista_required
def barista_dashboard(request):
    # Filter orders that are either in "Placed" or "In Preparation" status
    orders = Order.objects.filter(status__in=["Placed", "In Preparation", "Collected"])
    return render(request, 'orders/order/barista_dashboard.html', {'orders': orders})


"""Allows baristas to mark an order as collected"""
@barista_required
def mark_order_collected(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = "Collected"
        order.save()
        return redirect('barista_dashboard')  # Redirect back to the dashboard
    return render(request, 'orders/order/mark_order_collected.html', {'order': order})


"""Allow Barista to mark an order as 'Preparing'"""
@barista_required
def mark_order_preparing(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = "In Preparation"  # Update the order's status to 'In Preparation'
        order.save()
        return redirect('orders:barista_dashboard')  # Redirect back to the dashboard
    return render(request, 'orders/order/mark_order_preparing.html', {'order': order})


# Payment successful and order completion page
@login_required
def payment_completed(request):
    # Get the user's orders after payment completion
    user_orders = Order.objects.filter(user=request.user)

    # After successful payment
    return render(request, 'payment/completed.html', {'user_orders': user_orders})

