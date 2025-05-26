from django import forms


# This is a form class for user login: it is used to authenticate users against the database
class LoginForm(forms.Form):
    # Field for entering username
    username = forms.CharField()


    # Field for entering password.  Uses PasswordInput widget to hide the password characters on the webpage
    password = forms.CharField(widget=forms.PasswordInput)
