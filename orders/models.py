from django.conf import settings
from django.db import models

"""
This is an Order model. 
Contains fields to store customer information and a Boolean field 'paid', set to False by default.
"""


# Customer details
class Order(models.Model):
    # Fields for the database
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)

    # Status field for order progress
    PENDING = 'Pending'
    PREPARING = 'Preparing'
    COLLECTED = 'Collected'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PREPARING, 'Preparing'),
        (COLLECTED, 'Collected'),
    ]

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default=PENDING
    )
    # indexing
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created']), ]

    def __str__(self):
        return f'Order {self.id}'

    """
    Method to get the total cost of all items in the order
    """

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


    """
    Method to return the Stripe dashboard's URL for the payments associated with the order.
    If no payment ID is stored in the stripe_id field of the Order, an empty string is returned.
    """

    def get_stripe_url(self):
        if not self.stripe_id:
            # if there is no associated payment
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'  # Stripe path for test payments
        else:
            path = '/'  # Stripe path for real payments
        return f'https:dashboard.stripe.com{path}payments/{self.stripe_id}'
        # url = f'https://dashboard.stripe.com/test/payments/{obj.stripe_id}

        # Patterns for payments in the production env: https://dashboard.stripe.com/payments/{id}
        # test payments patterns:                      https://dashboard.stripe.com/payments/test/{id}


"""
Model to store the product, quantity and price paid for each item
"""


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        'shop.Product',
        related_name='order_items',
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    """
    Method to return the total amount paid for the order
    """

    def get_cost(self):
        return self.price * self.quantity
