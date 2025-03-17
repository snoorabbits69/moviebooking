from celery import Celery
import os

# Set the default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviebooking.settings')

app = Celery('moviebooking')

# Load Celery config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks
app.autodiscover_tasks()

# Define queues
app.conf.task_queues = {
    'default': {'exchange': 'default', 'routing_key': 'default'},
    'scheduler': {'exchange': 'scheduler', 'routing_key': 'scheduler'}
}

# Default queue for tasks
app.conf.task_default_queue = 'default'

# Route tasks to specific queues
app.conf.task_routes = {
    'movies.tasks.listen_for_expiry': {'queue': 'scheduler'},  
    'movies.tasks.handle_expired_seat': {'queue': 'default'},  
    'payments.tasks.payment_completed_email': {'queue': 'default'},
}

# Celery Beat schedule (Scheduler Task)
app.conf.beat_schedule = {
    'listen_for_expiry_periodically': {
        'task': 'movies.tasks.listen_for_expiry',
        'schedule': 10.0,  # Runs every 10 seconds
    },
}

# Set timezone
app.conf.timezone = 'UTC'
