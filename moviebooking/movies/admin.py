import datetime
from django.contrib import admin
from .models import Movie,Show,Seat,Room
import csv
from bookings.models import BookingSeats
from django.http import HttpResponse


def export_to_csv(modeladmin, request, queryset):
    show = queryset.first()  

    if not show:
        return HttpResponse("No show found", status=400)

    content_disposition = f'attachment; filename=seats_for_show_{show.id}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition

    writer = csv.writer(response)

    writer.writerow(['Seat Number', 'Booked','Booking_code','booking_id'])

    seats = show.seat_num.all()
     

    for seat in seats:
        booking_seat = BookingSeats.objects.filter(seat=seat.seat_num, show=show).first()
        booking_code = booking_seat.booking.booking_code if booking_seat else 'N/A'
        booking_id = booking_seat.booking.id if booking_seat else 'N/A'
        writer.writerow([seat.seat_num, seat.booked, booking_code,booking_id])

    return response

export_to_csv.short_description = 'Export Details about a Show'


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_filter=['created']
    

class SeatAdmin(admin.TabularInline):
    model=Seat    
  
    
@admin.register(Show)
class showAdmin(admin.ModelAdmin):
    inlines=[SeatAdmin]
    list_filter=['showtime']
    actions=[export_to_csv]
    
    
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_filter=["name"]