from decimal import Decimal
from django.conf import settings

class Ticket:
    def __init__(self, request):
        """Initialize ticket session."""
        self.session = request.session
        self.booking_id=None
        ticket = self.session.get(settings.TICKET_SESSION_ID)
        self.session.set_expiry(600)
        if not ticket:
            self.session[settings.TICKET_SESSION_ID] = {}
            ticket = self.session[settings.TICKET_SESSION_ID]
            
        
        self.ticket = ticket

    def add(self, seat):
        """Add a seat to the ticket session."""
        show_id = str(seat.show.id)

        if show_id not in self.ticket:
            self.ticket[show_id] = {
                'tickets': [],
                'price': float(seat.show.price),
            }
            

        if seat.seat_num not in self.ticket[show_id]['tickets']:
            self.ticket[show_id]['tickets'].append(seat.seat_num)

        print(self.total())  
        self.save()
        
        

    def remove(self, seat):
        """Remove a seat from the ticket session."""
        show_id = str(seat.show.id)

        if show_id in self.ticket and 'tickets' in self.ticket[show_id]:
            if seat.seat_num in self.ticket[show_id]['tickets']:
                self.ticket[show_id]['tickets'].remove(seat.seat_num)

                if not self.ticket[show_id]['tickets']:
                    del self.ticket[show_id]

        
        self.save()
    
    def __iter__(self):
        for show_id, show_data in self.ticket.items():
            yield {
                "show_id": show_id,
                "tickets": show_data["tickets"],
                "price": show_data["price"]
            }
        
    def total(self):
        total_price = Decimal('0.0')
        
        for show_id, show_data in self.ticket.items():
            ticket_count = len(show_data['tickets'])
            price = Decimal(str(show_data['price'])) 
            total_price += price * ticket_count  
        
        return float(total_price) 
    
    def clear(self):
     del self.session[settings.TICKET_SESSION_ID]
     self.save()


    def save(self):
        """Mark session as modified to ensure changes are saved."""
        self.session.modified = True
        print(self.ticket) 
