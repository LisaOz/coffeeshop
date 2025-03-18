# Form to authenticate users against the database
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  # Password widget is used to render the password HTML elem.
