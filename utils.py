def get_movie_names(cinema):
    movie_names = ""
    index = 0
    for m in cinema.movies:
        if index == 0:
            movie_names = m.movie_name.lower()
            index = 1
        else:
            movie_names = movie_names + "\n " + m.movie_name.lower()
    return movie_names


def get_schedule(movie, cinema):
    schedule = cinema.schedule
    schedule_movie = schedule[movie.movie_name.lower()]

    schedule_text = ""
    index = 1
    for s in schedule_movie:
        schedule_text = schedule_text + " say " + str(index) + " for going on " + s.day.lower() + " at " + str(
            s.time_slot) + " o' clock. \n"
        index = index + 1
    return schedule_text
