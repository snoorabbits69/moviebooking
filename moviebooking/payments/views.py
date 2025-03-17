from django.shortcuts import render,redirect
from django.urls import reverse
from tickets.ticket import Ticket
from bookings.models import Booking
import redis
import stripe
from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from .tasks import payment_completed_email
r=redis.Redis()


# Create your views here.
stripe.api_key=settings.STRIPE_SECRET_KEY
def payment_process(request):
   booking_id=request.session.get('booking_id')
   booked=Booking.objects.get(id=booking_id)
   print(booked.booking_items.all())
   if request.method == 'POST':
      success_url = request.build_absolute_uri(
            reverse('payment:completed',args=[booked.id])
        )
      cancel_url = request.build_absolute_uri(
            reverse('payment:failed')
        )
      session_data={
      'mode':'payment',
      'client_reference_id':booking_id,
      'success_url':success_url,
       'cancel_url':cancel_url,
       'line_items':[]
       }
      total_seats = booked.booking_items.count()
      for seat in booked.booking_items.all():
         session_data['line_items'].append({
            'price_data':{
               'unit_amount':int(seat.show.price * Decimal('100')),
               'currency':'usd',
               'product_data':{
                  'name':f"{seat.show}:{seat.show.start_date}:{seat.show.room.name}:{seat.seat}"
               }
            },
            'quantity':total_seats
         })
      session=stripe.checkout.Session.create(**session_data)
      return redirect(session.url, code=303)
      
   
   return render(request,"process.html")
    
    
def payment_completed(request,booking_id):
   payment_completed_email.delay(booking_id)
   return render(request,"completed.html")


def payment_failed(request):
   return render(request,"failed.html")

def payment_pdf(request,booking_id):
   book=Booking.objects.get(id=booking_id)
   print(book)
   return render(request,"pdf.html",{
      'booking':book
   })

  
    