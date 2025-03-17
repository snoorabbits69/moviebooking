from django.urls import path

from . import views
urlpatterns = [
    path('',views.MovieList,name="movie_list"),
    path('movie/<int:id>',views.MovieDetail,name="movie_detail"),
    path('movie/shows',views.AvailableShows,name='available_shows'),
    path('movie/shows/<str:currentdate>',views.AvailableShows,name='available_shows_withDate'),
    path('movie/bookings',views.movie_bookings,name='see_bookings'),
]
