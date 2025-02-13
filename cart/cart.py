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


        """
        Method to add products to the cart and update their quantity
        """
        def add(self, product, quantity=1, override_quantity=False):
            product_id = str(product.id) # product id a key in the product dictionary, convert is to string for JSON
            if product_id not in self.cart:
                self.cart[product_id] = {
                    'quantity': 0,
                    'price': str(product.price)
                }
            if override_quantity:  # a Boolean to indicate if the quantity has to be overridden with the given quantity
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save()

        """
        save() method marks the session as modified to tell Django that session was changed and needs to be saved
        """
        def save(self):
            self.session.modified = True

        """
           Method to remove products from the cart. Removes the given product from the cart dictionary 
           """

        def remove(self, product):
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()  # update the cart in the session




