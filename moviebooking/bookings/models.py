from django.db import models
from django.core.exceptions import ValidationError
from movies.models import Show,Seat
from django.conf import settings
import time
import random
import uuid


def generate_booking_id():
    timestamp = int(time.time() * 1000) % 100
    
    random_number = random.randint(10, 99)
    
    unique_part = uuid.uuid4().hex[:4]
    
    booking_id = f"{timestamp:02}{random_number}{unique_part}"
    
    return booking_id[:8]


class Booking(models.Model):
    booking_code = models.CharField(max_length=100,default=generate_booking_id())
    name = models.CharField(max_length=300)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  # Changed to auto_now=True for correct update timestamp
    paid = models.BooleanField(default=False)
    stripe_id=models.CharField(max_length=250,blank=True)
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.name
    
    def get_total_cost(self):
        return sum(item.show.price for item in self.booking_items.all() )
    
    def get_show(self):
        first_item = self.booking_items.first() 
        if first_item:
            return first_item.show  
        return None
    
    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '__test__' in settings.STRIPE_SECRET_KEY:
            path='/test/'
        else:
            path='/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'




class BookingSeats(models.Model):
    booking = models.ForeignKey(
        Booking, related_name="booking_items", on_delete=models.CASCADE
    )
    show = models.ForeignKey(
        Show, related_name="booked_seats", on_delete=models.CASCADE,null=True
    )
    seat = models.CharField(max_length=10,null=True)

   

