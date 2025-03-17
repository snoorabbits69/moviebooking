from django.urls import path
from . import views
from . import webhooks
app_name='payment'
urlpatterns = [
    path('process/',views.payment_process,name='process'),
    path('completed/<int:booking_id>',views.payment_completed,name='completed'),
    path('failed/',views.payment_failed,name='failed'),
     path('webhook/',webhooks.stripe_webhook,name='stripe-webhook'),
     path('ticket/<int:booking_id>',views.payment_pdf,name='pdf_payment'),
     
   
    

]

