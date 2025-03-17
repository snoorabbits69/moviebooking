import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import payment_completed_email
from bookings.models import Booking

@csrf_exempt
def stripe_webhook(request):
    payload=request.body
    sig_header=request.META['HTTP_STRIPE_SIGNATURE']
    event=None
    try:
        event=stripe.Webhook.construct_event(
            payload,sig_header,settings.STRIPE_WEBHOOK_SECRET
        )
        
    except ValueError:
     
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    if event.type=='checkout.session.completed':
        session=event.data.object
        if(session.mode=='payment' and session.payment_status=='paid'):
            try:
               booking=Booking.objects.get(
                   id=session.client_reference_id
               ) 
            except booking.DoesNotExist:
                return HttpResponse(status=404)
            print(booking.paid)
            booking.paid=True
            booking.stripe_id=session.payment_intent
            booking.save()
            payment_completed_email(booking.id)
        return HttpResponse(status=200)
   