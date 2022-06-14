import random

import numpy as np


class Cinema:
    def __init__(self, cinema_name, movies, rooms):
        self.cinema_name = cinema_name
        self.movies = movies
        self.rooms = rooms
        self.make_schedule()
        self.reservations = dict()

    def make_schedule(self):
        time_slots = list(np.arange(10, 22, 1))
        print(time_slots)
        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        schedule_dict = dict()
        for movie in self.movies:
            schedule = []
            days = random.sample(week_days, movie.popularity)
            for d in days:
                room = random.sample(self.rooms, 1)[0]
                time_slot = random.sample(time_slots, 1)[0]
                schedule.append(Schedule(d, room, time_slot))
                schedule_dict[movie.movie_name.lower()] = schedule
        self.schedule = schedule_dict

    def make_reservation(self, name, movie_name, n_persons, day, time):
        if movie_name not in self.reservations.keys():
            self.reservations[movie_name.lower()] = []

        reservation = Reservation(name, n_persons, day, time)
        s = reservation.get_schedule_availability(self.schedule[movie_name])
        if s is not None:
            s.room.n_reserved = s.room.n_reserved + n_persons
            reservation.room = s.room
            self.reservations[movie_name.lower()].append(reservation)
            return True
        else:
            return False


class Schedule:
    def __init__(self, day, room, time_slot):
        self.day = day
        self.room = room
        self.time_slot = time_slot


class Movie:
    def __init__(self, movie_name, duration, popularity):
        self.movie_name = movie_name
        self.duration = duration
        self.popularity = popularity


class Room:
    def __init__(self, room_id, n_seats, n_reserved=0):
        self.room_id = room_id
        self.n_seats = n_seats
        self.n_reserved = n_reserved


class Reservation:
    def __init__(self, name, n_persons, day, time_slot):
        self.name = name
        self.n_persons = n_persons
        self.time_slot = time_slot
        self.day = day
        self.room = None

    def get_schedule_availability(self, schedule):
        for s in schedule:
            if self.day == s.day and self.time_slot == s.time_slot:
                if s.room.n_reserved + self.n_persons > s.room.n_seats:
                    return None
                else:
                    return s
