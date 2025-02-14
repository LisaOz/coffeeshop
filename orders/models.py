from django.conf import settings
from django.db import models

"""
This is an Order model. 
Contains fields to store customer information and a Boolean field 'paid', set to False by default.
"""


# Customer details
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)


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
