from io import BytesIO
import weasyprint
from celery import shared_task
from django.contrib. staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order


"""
Create a task to send the email with the notification that an order has been successfully paid.
Decorator @shared_task is used to define the payment_completed task.
"""
@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)

    # create email with the receipt
    subject = f'Coffee Shop. Receipt No {order.id}'
    message = 'Your receipt for the recent purchase'

    # EmailMessage class (provided by Django) is used to create an email object
    email = EmailMessage(subject, message, 'admin@coffeeshop.com', [order.email])

    # Generate PDF from the rendered template
    html = render_to_string('orders/order/pdf.html', {'order': order})

    # Output the PDF file to a BytesIO instance
    out = BytesIO() # in-memory bytes buffer
    stylesheets = [weasyprint.CSS(finders.find('css/pdf.css'))]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # Attach the generated PDF to the email
    filename = f'order_{order.id}.pdf'
    email.attach(filename, out.getvalue(), 'application/pdf')

    # Modify console output to show only the attachment name
    print(f"\n--- EMAIL SENT ---")
    print(f"Subject: {email.subject}")
    print(f"From: {email.from_email}")
    print(f"To: {', '.join(email.to)}")
    print(f"Message: {email.body}")

    # Show the attachment name instead of full content
    print("\n--- ATTACHMENTS ---")
    print(f"Attachment: {filename}")

    # Send the email (it will be printed to the console)
    email.send()
