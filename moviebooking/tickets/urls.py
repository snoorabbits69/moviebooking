from django.urls import path
from . import views
app_name='tickets'
urlpatterns = [
    path('add/<int:seat_id>',views.ticket_add,name='ticket_add')
]
