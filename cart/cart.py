from django.conf import settings
from decimal import Decimal
from shop.models import Product

# Cart class that allow the user to manage the shopping cart
class Cart:
    def __init__ (self, request):
        self.session = request.session # initialise the cart with a request object
        cart = self.session.get(settings.CART_SESSION_ID) # store the current session to allow other Cart methods use it

        # If no cart present in the session, create an empty cart with an empty dictionary and product ID key
        # a dictionary will a value that includes quantity and price to guarantee that a product will only be added once
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
