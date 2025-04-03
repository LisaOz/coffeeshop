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


"""
Test case for placing an order.
Verifies that an order is created correctly with order items and the correct status.
"""


class OrderModelTest(TestCase):
    def test_place_order(self):


        # Step 1: Create a test user
        user = User.objects.create_user(username='test_user', password='password123')

        # Step 2: Create a test product
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=Category.objects.create(name="Test Category", slug="test-category"),
            price=10.00,
            description="A test product for orders"
        )

        # Step 3: Create an Order instance
        order = Order.objects.create(
            user=user,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            address="123 Test St",
            postal_code="12345",
            city="Test City"
        )

        # Step 4: Add the product to the order (OrderItem)
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=2
        )

        # Step 5: Test if order status is 'Pending' by default
        self.assertEqual(order.status, 'Pending', f"Expected 'Pending', got {order.status}")

        # Step 6: Test if total cost is calculated correctly
        expected_total_cost = product.price * order_item.quantity
        self.assertEqual(order.get_total_cost(), expected_total_cost,
                         f"Expected {expected_total_cost}, got {order.get_total_cost()}")

        # Step 7: Test Stripe URL when no stripe_id is set
        self.assertEqual(order.get_stripe_url(), '', "Stripe URL should be empty when stripe_id is not set")

        # Step 8: Simulate payment by setting order as paid and changing status
        order.paid = True
        order.status = 'Preparing'
        order.save()

        # Step 9: Test that the order is marked as 'Preparing' and paid is set to True
        order.refresh_from_db()  # Refresh to get the updated values
        self.assertEqual(order.status, 'Preparing', f"Expected 'Preparing', got {order.status}")
        self.assertTrue(order.paid, "Expected 'paid' to be True")

        # Step 10: Test Stripe URL after payment
        order.stripe_id = "test_stripe_id"
        order.save()

        stripe_url = order.get_stripe_url()
        expected_stripe_url = 'https://dashboard.stripe.com/test/payments/test_stripe_id'
        self.assertEqual(stripe_url, expected_stripe_url, f"Expected {expected_stripe_url}, got {stripe_url}")

        # Clean up (optional)
        order_item.delete()
        order.delete()
        product.delete()
        user.delete()
