from .cart import Cart
"""
This is a context processor to set the current cart in the request context.
It will allow to access the cart in any template.
"""


def cart(request):
    return {'cart': Cart(request)}  # Initiate the cart using the request object
