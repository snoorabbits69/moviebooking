from celery import shared_task
from bookings.models import Booking
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO
from django.contrib.staticfiles import finders

@shared_task(queue='default')
def payment_completed_email(booking_id):
    print("Running email task...")
    try:
        booking = Booking.objects.filter(id=booking_id).first()
        if not booking:
            return f"Order with ID {booking_id} does not exist."

        subject = f'Ticket for movie {booking.booking_code}'
        message = 'Please get this to watch the movie'
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email="snoorabbits69@gmail.com",
            to=[booking.email]
        )

        html = render_to_string('pdf.html', {'booking': booking})
        out = BytesIO()
        pdf_styles = finders.find('css/pdf.css')

        if pdf_styles:
            stylesheets = [weasyprint.CSS(pdf_styles)]
        else:
            stylesheets = []

        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
        out.seek(0)
        
        email.attach('ticket.pdf', out.getvalue(), 'application/pdf')

        email.send(fail_silently=False)
        return f"Email sent successfully to {booking.email}"

    except Exception as e:
        return f"An error occurred: {str(e)}"
