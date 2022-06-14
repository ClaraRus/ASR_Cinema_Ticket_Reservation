from movies.models import Cinema, Room, Schedule
from movies.models import Movie

movies = [Movie("Batman", 120, 7), Movie("Encanto", 120, 5), Movie("Spiderman", 120, 3), Movie("Sonic", 120, 3), Movie("Ambulance", 120, 3), Movie("Doctor Strange", 120, 3)]
rooms = [Room(1, 100), Room(2, 50), Room(3, 30)]
cinemas = [Cinema("New York", movies, rooms), Cinema("New Jersey", movies, rooms)]

def add_movies(cinema_obj):
    movies_model = []
    for movie_obj in cinema_obj.movies:
        movie_model = Movie.objects.create(movie_name=movie_obj.movie_name, duration=movie_obj.duration,
                                           popularity=movie_obj.popularity)
        movies_model.append(movie_model)
    return movies_model


def add_rooms(cinema_obj):
    rooms_model = []
    for room_obj in cinema_obj.rooms:
        print(room_obj.room_id)
        room_model = Room.objects.create(room_id=room_obj.room_id, n_seats=room_obj.n_seats,
                                         n_reserved=room_obj.n_reserved)
        rooms_model.append(room_model)
    return rooms_model


def add_data(cinemas):
    cinema_models = []

    for cinema_obj in cinemas:
        print(cinema_obj.cinema_name)
        # movies_model = add_movies(cinema_obj)
        # rooms_model = add_rooms(cinema_obj)

        cinema_model = Cinema.objects.create(name=cinema_obj.cinema_name)
        cinema_models.append(cinema_model)
    return cinema_model  # , movies_model, rooms_model


def create_schedule():
    schedule_models = []
    room_models = dict()
    cinema_models = []
    movie_models = []
    for cinema_obj in cinemas:
        schedule = cinema_obj.schedule
        for item in schedule.items():
            if not cinema_obj.cinema_name in cinema_models:
                cinema_model = Cinema.objects.create(name=cinema_obj.cinema_name)
                cinema_models.append(cinema_obj.cinema_name)

            movie_obj = [m for m in cinema_obj.movies if m.movie_name.lower() == item[0].lower()][0]
            if not movie_obj.movie_name in movie_models:
                movie_model = Movie.objects.create(movie_name=movie_obj.movie_name, duration=movie_obj.duration,
                                                   popularity=movie_obj.popularity)
                movie_models.append(movie_obj.movie_name)
            else:
                movie_model = Movie.objects.get(movie_name=movie_obj.movie_name)
            for schedule in item[1]:
                day, room_obj, time_slot = schedule.day, schedule.room, schedule.time_slot

                if not room_obj.room_id in room_models.keys():
                    room_model = Room.objects.create(room_id=room_obj.room_id, n_seats=room_obj.n_seats,
                                                     n_reserved=room_obj.n_reserved)
                    room_models[room_obj.room_id] = room_model

                schedule_model = Schedule.objects.create(cinema=cinema_model, movie=movie_model,
                                                         room=room_models[room_obj.room_id], day=day,
                                                         time_slot=time_slot)
                schedule_models.append(schedule_model)


