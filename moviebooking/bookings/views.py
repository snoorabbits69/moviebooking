from django.shortcuts import render, get_list_or_404, get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt

from movies.models import Seat, Show
from django.urls import reverse
from tickets.ticket import Ticket
from .forms import BookingForm
from django.views.decorators.http import require_POST
from .models import Booking,BookingSeats
import redis
import json

r = redis.Redis()








@csrf_exempt
def book_show(request, id, movie):
    seats = get_list_or_404(
        Seat,
        show=id
    )
    show = get_object_or_404(
        Show,
        id=id
    )
    form=BookingForm()
    if request.user.is_authenticated:
        user = request.user
        initial_data = {'email': user.email, 'name': user.username}
        form=BookingForm(initial_data)
 
    
    
   
    if request.method == "POST":
        ticket=Ticket(request)
        seat_data = json.loads(request.body)
        seat_num = seat_data['seat']  
       
        if seat_data['add']=="True":
            r.set(f"{show.id}:{show.start_date}:{show.room.name}:{seat_num}", seat_num, 360)
            
            seat = get_object_or_404(
                Seat,
                show=show,
                seat_num=seat_num
            )
            seat.booked = True
            seat.save()
            ticket.add(seat)
            
        else:
            r.delete(f"{show.id}:{show.start_date}:{show.room.name}:{seat_num}")
            
            seat = get_object_or_404(
                Seat,
                show=show,
                seat_num=seat_num
            )
            seat.booked = False
            seat.save()
            ticket.remove(seat)
        
        
    
    return render(request, 'booking/Booking.html', {
        'seats': seats,
        'show': show,
        'form':form
    })


@require_POST
def booking_create(request):
    tickets = Ticket(request)
    print(tickets.total())
    
    for show in tickets:
        show_id = show['show_id']
        seats = show['tickets']
        price = show['price']
    
    show = Show.objects.get(id=show_id)
    
    form = BookingForm(request.POST)
    if form.is_valid():
        booked = form.save(commit=False)
        booked.save()
        for seat in seats:
            print(seat)
            BookingSeats.objects.create(
                booking=booked,
                show=show,
                seat=seat
            )
        tickets.clear()
        request.session['booking_id'] = booked.id
        print(booked.id, 'Book')
        
        return redirect('payment:process')
    

 