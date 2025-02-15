from cart.cart import Cart
from django.shortcuts import render
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


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

            # redirect to the order created page
            #
            return render(
                request, 'orders/order/created.html', {'order': order}
            )
    else:
        form = OrderCreateForm()


    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )
