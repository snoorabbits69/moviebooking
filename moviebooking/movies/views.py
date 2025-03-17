from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Movie,Show
from bookings.models import Booking
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def MovieList(request):
    movies=Movie.objects.all()
    return render(request, "movie/list.html", {
        "route": "home",
        "movies":movies
    })
    
def MovieDetail(request,id):
    movie=get_object_or_404(
        Movie,
        id=id
    )
    print(movie)
    return render(request,"movie/detail.html",{
        "movie":movie
    })
    




@csrf_exempt
def AvailableShows(request, currentdate=None):
    if currentdate:
        currentdate = parse_date(currentdate)  
    else:
        currentdate = datetime.date.today()  

    shows = Movie.objects.filter(
        show_times__isnull=False,
        show_times__start_date__lte=currentdate,
        
    ).distinct()
   
    
    if not shows.exists():
        shows=None
    if request.method=='POST':
        print(request.body)

    return render(request, 'shows/list.html', {
        'shows': shows,
        'currentdate': currentdate.isoformat()
    })
    




def movie_bookings(request):
    booking = None
    error_message = None
    seats = []
    mybookings=[]
    if request.user.is_authenticated:
        user_email=request.user.email
        print(user_email)
        mybookings=Booking.objects.filter(email=user_email)
        
    
    
    if request.method == 'POST':
        cd = request.POST
        booking_code = cd.get('bookingcode')

        if booking_code:
            try:
                # Fetch the booking object based on the booking code
                booking = Booking.objects.get(booking_code=booking_code)
                # Fetch related seat data (adjust based on your actual model relationships)
                seats = booking.booking_items.all()
            except Booking.DoesNotExist:
                error_message = "No booking found with the provided booking code"
        else:
            error_message = "Please enter a booking code"

    if seats:
        first_show = seats[0].show  
    else:
        first_show = None  

    return render(request, 'shows/bookings.html', {
        'booking': booking,
        'seats': seats, 
        'error_message': error_message,
        'mybookings':mybookings
    })





    