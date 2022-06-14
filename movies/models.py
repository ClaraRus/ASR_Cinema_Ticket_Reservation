
# movies/models.py
from django.db import models


class Movie(models.Model):
    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    movie_name = models.CharField(max_length=50)
    duration = models.PositiveSmallIntegerField(unique=False)
    popularity = models.PositiveSmallIntegerField(unique=False)


class Room(models.Model):
    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    room_id = models.PositiveSmallIntegerField(unique=True)
    n_seats = models.PositiveSmallIntegerField(unique=False)
    n_reserved = models.PositiveSmallIntegerField(unique=False)


class Cinema(models.Model):
    class Meta:
        verbose_name = 'Cinema'
        verbose_name_plural = 'Cinemas'

    name = models.CharField(max_length=50)


class Reservation(models.Model):
    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    name = models.CharField(max_length=50)
    n_persons = models.PositiveSmallIntegerField(unique=False)
    time_slot = models.CharField(max_length=50)
    day = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Schedule(models.Model):
    class Meta:
        verbose_name = 'Show'
        verbose_name_plural = 'Shows'

    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    day = models.CharField(max_length=50)
    time_slot = models.CharField(max_length=50)
