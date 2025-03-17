from django.shortcuts import render,get_object_or_404
from .ticket import Ticket
from django.views.decorators.http import require_POST
from movies.models import Show



# Create your views here.
@require_POST
def ticket_add(request,seat_id):
    ticket=Ticket(request)
    seat=get_object_or_404(Show,id=seat_id)
    ticket.add(seat_id)
    return "good"
    
    