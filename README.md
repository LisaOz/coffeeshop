# Coffee Shop Website

## Table of Contents

1. [Introduction](#introduction)
2. [Project Setup](#project-setup)
3. [Installed Dependencies](#installed-dependencies)
4. [Application Structure](#application-structure)
5. [User Interface](#user-interface)
6. [Admin Interface](#admin-interface)
7. [Features](#features)
8. [Third-Party Integrations](#third-party-integrations)
9. [Running the Project](#running-the-project)
10. [Testing](#testing)
11. [License](#license)

---

## Introduction

Welcome to the **Coffee Shop Website**! 
<br>
<br>
This project is a fully functional web application built to provide a seamless and user-friendly experience for the customers and administrators. 
While it is ready to be deployed, it is still in the development phase. 
The application allows users to browse a menu, place orders, and make payments with integrated features like Stripe for payment processing and Celery with RabbitMQ for handling asynchronous tasks such as sending payment notifications and emails with receipts.

This project demonstrates essential web application features, including user and admin interfaces, product management, order processing, and notifications.

---

## Project Setup

Ensure you have the following necessary packages installed:
- Python 3.x
- Django
- Celery
- RabbitMQ
- Stripe account (for payment integration)
- Redis (for Celery's message broker)

You can install the required dependencies from the requirements.txt file.

To set up the project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/LisaOz/coffeeshop.git
   cd coffeeshop

2. **Create a virtual environment and activate it**:
   

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate  # For Windows

3. **Install the required dependencies if they are not yet installed:**

   ```bash
   pip install -r requirements.txt

4. **Set up the environment variables**
   
   Create a .env file in the root directory and include the sensitive settings such as:

   - SECRET_KEY
   - DEBUG
   - STRIPE_API_KEY
   - DATABASE_URL

5. **Run the database migrations**:

   ```bash
   python manage.py migrate

6. **Create a superuser for the admin panel**:

   ```bash
   python manage.py createsuperuser

## Installed Dependencies

   This project uses the following dependencies:

   - **Django** - A high-level Python web framework used for building web applications.
   - **Celery** - Asynchronous task queue/job queue used for handling background tasks (such as sending emails, generating PDFs).
   - **RabbitMQ** - Message broker used as a message transport for Celery.
   - **Stripe** - Payment gateway integration for handling secure payments.
   - **WeasyPrint** - For generating PDF receipts.

## Application Structure

   ### File and Folders:
   
   - **coffeeshop/** - Root folder containing project settings, configurations, and global dependencies.
   - **cart/** - Application that handles the shopping cart functionality, including adding, updating, and removing items.
   - **orders/** - Application that manages order processing, including order creation, status tracking, and history.
   - **payment/** - Application that handles payment processing, integrations with payment gateways, and contains webhooks and background tasks for transaction management.
   - **shop/** - Application that manages product listings, categories, and contains templates for displaying the list of products and products details.

   ### Files Contained in the Application Directories:
   
   - **models.py** - Defines the database models for products, orders, and cart items.
   - **views.py** - Handles the logic website pages, such as displaying products, cart interactions, and checkout.
   - **tasks.py** - Contains Celery tasks for background processing, including sending confirmation emails and handling delayed transactions.
   - **urls.py** - Defines URL routes for different application views, such as product pages, checkout, and order history.
   - **templates/** - HTML templates for the user interface, including products page, order and payment confirmations, and receipts
   - **static/** - Stores static assets such as images and CSS file for styling and functionality.

## User Interface
The user interface provides the following functionalities:

- **Home Page**: Displays the coffee shop's menu with the  option to select items.
- **Order Page**: Allows users to select products, provide details, and submit an order.
- **Stripe Integration**: Users can securely pay for their orders via Stripe.
- **Order Confirmation**: After payment, users receive a PDF receipt via email.

## Admin Interface

The Django admin interface provides the following features for administrators:
- **Admin Dashboard**: An easy to use admin interface provided by Django for managing orders and products.
- **Manage Orders**: Admins can view, edit, and delete orders.
- **Manage Products**: Admins can add, edit, or remove products from the menu.
- **View Customer Details**: Admins can see customer information associated with each order.
- **Handle Payments**: Admins can track the status of payments via Stripe.
  Other Features:
- **Order Placement**: Users can place orders online with the user-friendly interface.
- **Stripe Payments**: Secure and easy-to-use payment processing through Stripe.
- **Celery for Asynchronous Tasks**: Tasks such as order confirmation messages and sending email notifications about successfult payments are handled in the background.
- **PDF Receipts**: Orders are confirmed with a PDF receipt that is sent to the user’s email. This feature is implemented with the console output and can be modified for    sending emails by changing the EMAIL_BACKEND in the project's settings.


## Third-Party Integrations

- **Stripe**: Stripe API is used for processing payments securely. 
- **Celery**: Used for handling background tasks like sending emails and generating PDF receipts.
- **RabbitMQ**: Celery uses RabbitMQ as the message broker for task management.
- **WeasyPrint**: Used to generate PDF receipts for orders.

## Running the Project
   ### Running the Development Server
   To run the development server locally:

1. **Start the Django server**:
      ```bash
      python manage.py runserver
2. Access the website at http://127.0.0.1:8000/. Access the administration site at http://127.0.0.1:8000/admin/ with the superuser credentials.
   

3. **Running Celery**
   To run Celery with RabbitMQ as the message broker:

   Start RabbitMQ or make sure RabbitMQ is running. You can start RabbitMQ in the Dockers container or from the separate terminal with the following command (depending on the OS):

      ```bash
      sudo rabbitmq-server start

   Open http://127.0.0.1:15672 to acces RabbitMq messagment UI and see the queued messages.
   Run Celery worker: enter the folder where manage.py is located, activate the virtual environment .\venv\Scripts\Activate and run Celery:

      ```bash
      celery -A coffeeshop worker --loglevel=info --pool=solo 

5. **Monitoring Celery with Flower**
   
   Flower is another tool, besides of RabbitMQ, to monitor the asynchronous tasks executed with Celery. Run it from the separate terminal after activating the virtual environment:
   ``` bash
   celery -A coffeeshop flower
   
   To monitor Celery with Flower, access it on the page: http://localhost:5555:


## Stripe Integration

   This project uses [Stripe](https://stripe.com/) to handle secure transactions and payment confirmations.
   Stripe provides an API (Application Programming Interface) that allows developers to integrate payment processing into their applications.
   It offers a set of RESTful APIs that handle transactions, refunds, subscriptions, webhooks, and more.

   ### Stripe's API includes:

   Payment API – For handling card payments, digital wallets, and bank transfers.
   Checkout API – A hosted payment page for quick integration.
   Connect API – For managing multi-vendor platforms (like marketplaces).
   Billing API – For handling subscriptions and invoicing.
   Webhook API – For receiving real-time notifications about payment events.
   
   To integrate the payment gateway into the site, following steps have to be taken:
   1. Setting a Stripe account. Follow this link to set the account: https://dashboard.stripe.com/register
   2. Setting the Stripe API keys in the .env file.
   3. Frontend code can be used to handle Stripe’s JavaScript library for payment processing.


   ### Features:
   
   - Customers can securely pay for their orders using Stripe.  
   - Order details are stored, and a receipt is generated upon successful payment.  
   - Webhooks are implemented to listen for Stripe events, ensuring that order statuses are updated accordingly.  
   - The webhook handler processes payment events, such as successful charges, and updates the database automatically.  

## Webhooks Configuration: 

   1. Configure your webhook endpoint in the Stripe Dashboard under **Developers > Webhooks**.  
   2. Set the webhook URL to:  
      https://your-ngrok-url.ngrok.io/stripe/webhook/ (in development).
   3. Ensure that the webhook secret key is set in the environment variables (e.g., using `python-decouple`).  
   4. Stripe will send event notifications to the provided endpoint.


## Acknowledgements
   
I would like to express my gratitude to **Antonio Mele** for his guidance and insights provided in the book "Django 5 by example", which was a helpful tool in the    development of this coffeeshop website.


## License

This project is licensed under the **MIT License**
