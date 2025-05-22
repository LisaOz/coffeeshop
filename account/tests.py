from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


"""
Test case for creating an account 
Verifies that a user account is created successfully
"""


class AccountTests(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('account:register'), {
            'username': 'testuser',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
        })


        self.assertRedirects(response, reverse('shop:product_list'))


    """
    Test case for logging in with valid credentials
    """

    def test_login_with_valid_credentials(self):
        user = User.objects.create_user(username='testuser', password='StrongPassword123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongPassword123',
        })

        self.assertRedirects(response, reverse('account:dashboard'))



        """
        Test case for logging in with invalid credentials
        """

        def test_login_with_invalid_credentials(self):
            response = self.client.post(reverse('login'), {
                'username': 'wronguser',
                'password': 'wrongpass',
            })
            self.assertContains(response, "Please enter a correct username and password", status_code=200)