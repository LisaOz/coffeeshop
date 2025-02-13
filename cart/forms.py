# Form to add products to the cart

from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class FormToAddProduct(forms.Form):
    quantity = forms.TypedChoiceField( # allows the user to select quantity in range 1-20
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput # not to display to the user
    )
