from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Product, Category
from orders.models import Order, OrderItem

"""
Test for the Product model: adding a new product to the database
"""


class ProductModelTest(TestCase):
    def test_product_creation(self):
        # Create a category
        category = Category.objects.create(name='Drinks', slug="drinks")

        #  Create a product that belongs to the category
        product = Product.objects.create(
            name='Coffee',
            slug="coffee",
            price=9.99,
            description='A delicious coffee',
            category=category  # Assign the category
        )
        self.assertEqual(product.name, 'Coffee')
        self.assertEqual(product.price, 9.99)
        self.assertEqual(product.description, 'A delicious coffee')
        self.assertEqual(product.category, category)  # Ensure the Category is assigned
        self.assertIsNotNone(product.id)  # Ensure the product was saved to the database