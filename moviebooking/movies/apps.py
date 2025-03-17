from django.apps import AppConfig


class MoviesConfig(AppConfig):
    name = 'movies'  # The name of your app
    default_auto_field = 'django.db.models.BigAutoField'  # This is for Django 3.2+ (if not specified)

  