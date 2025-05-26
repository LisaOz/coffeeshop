# Form to add products to the cart

from django import forms

# Create a list of tuples for quantity choices (1 to 20)
# Each tuple is in the format (value, display_label)

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


# Class Form: defines a form to add a product to the cart

class FormToAddProduct(forms.Form):
    # Quantity field allows the user choose a number between 1 and 20
    # 'coerce=int' converts the selected value to an integer
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )

    # Override field: hidden checkbox to indicate whether to replace existing quantity
    # False on default
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput  # does not to display to the user
    )
