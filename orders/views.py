from cart.cart import Cart
from django.shortcuts import render
from .forms import OrderCreateForm
from .models import OrderItem


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

            # redirect to the order created page
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
