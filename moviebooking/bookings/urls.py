from django.urls import path
from . import views
urlpatterns = [
 path('<int:id>/<str:movie>',views.book_show,name='book_show'),
path('checkout',views.booking_create,name='checkout')
]
