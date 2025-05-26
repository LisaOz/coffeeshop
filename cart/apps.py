from django.apps import AppConfig


# Define configuration for the 'cart' application
class CartConfig(AppConfig):
    # Specify the default type for auto-generated primary keys in this app's models
    default_auto_field = 'django.db.models.BigAutoField'

    # Set the name of the app
    name = 'cart'
