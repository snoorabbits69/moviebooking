
from django.urls import path
from django.contrib.auth import views as auth_views,login
from .import views
urlpatterns = [
    path('login',auth_views.LoginView.as_view(),name='login'),
    path('register',views.RegisterView.as_view(),name='register'),
    path('logout',auth_views.LogoutView.as_view(template_name='registration/logged_out.html'),name="logout"),
]
