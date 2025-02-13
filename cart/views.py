from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import FormToAddProduct


"""
Create views to add items to the cart, update quantities, remove items from the cart cna display the cart's contents
"""
"""
This view is for adding products to the cart and updating the existing products number
"""


@require_POST  # only POST requests are allowed
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = FormToAddProduct(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
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
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


"""
View to display the cart with its contents
"""


def cart_detail(request):
    cart = Cart(request)
    # iterate the items in the cart and allow the quantity of each to be changed
    for item in cart:
        item['update_quantity_form'] = FormToAddProduct(
            initial={'quantity': item['quantity'], 'override': True} # allow to override the initial quantity
        )

    return render(request, 'cart/detail.html', {'cart': cart})
