from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from .models import Seat
import redis
import time

# Redis connection
r = redis.Redis()

@shared_task(queue='default')
def handle_expired_seat(key):
    """Processes expired seat reservation based on Redis key expiration."""
    try:
        key_str = key.decode('utf-8') if isinstance(key, bytes) else key
        parts = key_str.split(":")  # Ensure it's always a string

        if len(parts) < 4:
            print(f"Invalid key format: {key}")
            return
        
        show_id, start_date, room_name, seat_num = parts
        
        # Get the seat object from the database
        seat = Seat.objects.get(seat_num=seat_num, show_id=show_id)
        seat.booked = False
        seat.save()
        print(f"Seat {seat_num} for show {show_id} marked as available.")
        
    except ObjectDoesNotExist:
        print(f"Seat with seat_num {seat_num} does not exist or was already removed.")
    except Exception as e:
        print(f"Error handling expired seat: {e}")

@shared_task(queue='scheduler')
def listen_for_expiry():
    """Periodically checks Redis for expired keys."""
    pubsub = r.pubsub()
    pubsub.psubscribe('__keyevent@0__:expired')

    print("Checking for expired keys...")
    end_time = time.time() + 5  # Run for 5 seconds and exit
    while time.time() < end_time:
        message = pubsub.get_message()
        if message and message['type'] == 'pmessage':
            key = message['data']
            print(f"Expired key detected: {key}")

            # Trigger the expired seat handler asynchronously
            handle_expired_seat.delay(key)

        time.sleep(1)  # Avoid excessive CPU usage

    print("Listener stopped.")
