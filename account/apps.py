from django.apps import AppConfig

# Define configuration for the 'account' app
class AccountConfig(AppConfig):
    # Set the default type of primary key field for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # Specify the name of this app as 'account'
    name = 'account'
