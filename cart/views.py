from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import FormToAddProduct


"""
Views to add items to the cart, update quantities, remove items from the cart cna display the cart's contents
"""

"""
This view is for adding products to the cart and updating the existing products number
"""


@require_POST  # only POST requests are allowed for this view
def cart_add(request, product_id):
    cart = Cart(request)  # Get cart from the session
    product = get_object_or_404(Product, id=product_id)  # Get the product or raise a 404 error
    form = FormToAddProduct(request.POST)  # bind the form with the data

    # Check if the form is valid
    if form.is_valid():
        cd = form.cleaned_data  # If the form is valid, get the cleaned data

        # Add the product to the cart
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')  # redirects to the cart_detail URL which displays the contents of the cart


"""
View to remove items from the cart
"""


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)  # get the cart from the session
    product = get_object_or_404(Product, id=product_id)  # get the product or raise a 404 error
    cart.remove(product)  # remove the product
    return redirect('cart:cart_detail')  # redirect to the cart_detail URL


"""
This is aView to display the cart with its contents
"""


def cart_detail(request):
    cart = Cart(request)  # get the cart from the session
    # iterate the items in the cart and allow the quantity of each to be changed
    for item in cart:
        item['update_quantity_form'] = FormToAddProduct(
            initial={'quantity': item['quantity'], 'override': True} # allow to override the initial quantity
        )
    # render the cart detail page with the current cart contents
    return render(request, 'cart/detail.html', {'cart': cart})
