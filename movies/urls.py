# movies/urls.py
from django.urls import path

from . import views

urlpatterns = [
  path('answer', views.choose_cinema, name='choose_cinema'),
  path('choose_movie', views.choose_movie, name='choose_movie'),
  path('choose_schedule', views.choose_schedule, name='choose_schedule'),
  path('user_details', views.user_details, name='user_details'),
  path('make_reservation', views.user_details, name='make_reservation'),
  path('confirm_reservation', views.user_details, name='confirm_reservation'),
]