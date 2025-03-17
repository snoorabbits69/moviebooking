from .ticket import Ticket

def ticket(request):
    return {'ticket':Ticket(request)}