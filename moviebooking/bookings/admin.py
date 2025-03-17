from django.contrib import admin
from .models import Booking,BookingSeats
from django.http import HttpResponse
import csv
def export_bookings_to_csv(modeladmin,request,queryset):
  bookings=queryset
  if not bookings:
    return HttpResponse("No show found", status=400)
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition']='attachment;filename="bookings.csv"'
  writer = csv.writer(response)
  row_heads = ['id', 'booking_code', 'booking_user', 'booking_email', 'paid', 'stripe_id', 'show_name','show_date','show_time', 'show_room', 'booked_seats','Total']
  writer.writerow(row_heads)
  
  for booking in bookings:
      booked_seats = booking.booking_items.all()
      seat_info = "; ".join([
            seat.seat
            for seat in booked_seats
        ])
      writer.writerow([
            booking.id,
            booking.booking_code,
            booking.name,
            booking.email,
            booking.paid,
            booking.stripe_id,
            booked_seats[0].show.movie if booked_seats else "N/A",
            booked_seats[0].show.start_date if booked_seats else "N/A",
            booked_seats[0].show.showtime if booked_seats else "N/A",
            booked_seats[0].show.room.name if booked_seats else "N/A",
            seat_info,
            booking.get_total_cost()
        ])
  return response



export_bookings_to_csv.short_description='Export the bookings detail to csv'


class BookingAdminInline(admin.TabularInline):
    model = BookingSeats
    list_filter = ["booked_date"]

@admin.register(Booking)
class BookingUserAdmin(admin.ModelAdmin):
    inlines = [BookingAdminInline]
    actions=[export_bookings_to_csv]
    list_filter = ["created"]
    

 
    

