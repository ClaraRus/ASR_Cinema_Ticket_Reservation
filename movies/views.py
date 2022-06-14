from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.voice_response import VoiceResponse
from word2number import w2n

from .models import Movie, Cinema, Schedule

@csrf_exempt
def choose_cinema(request: HttpRequest) -> HttpResponse:
    vr = VoiceResponse()
    vr.say('Welcome to the cinema reservation system!')

    with vr.gather(
            action=reverse('choose_movie'),
            input='speech',
            timeout=3,
            speech_model='numbers_and_commands'
    ) as gather:
        gather.say('Please say the name of the cinema from the list:')
        cinemas = (
            Cinema.objects.all()
        )
        for cinema in cinemas:
            gather.say(f'{cinema.name}')

    vr.say('We did not receive your selection')
    vr.redirect('')

    return HttpResponse(str(vr), content_type='text/xml')


@csrf_exempt
def choose_movie(request: HttpRequest) -> HttpResponse:
    vr = VoiceResponse()
    name = request.POST.get('SpeechResult')
    if name is not None:
        name = name.strip('.')
    try:
        cinema = Cinema.objects.get(name=name)

    except Cinema.DoesNotExist:
        vr.say('Please select a cinema from the list.')
        vr.redirect(reverse('choose-cinema'))

    else:
        cinema_name = cinema.name.replace(' ', '%20')
        print(f'{reverse("choose_schedule")}?cinema={cinema_name}')
        with vr.gather(
                action=f'{reverse("choose_schedule")}?cinema={cinema_name}',
                input='speech',
                timeout=3,
                speech_model='numbers_and_commands',
        ) as gather:
            gather.say('Please say the name of the movie from the list:')
            movies = (
                Movie.objects.all()
            )
            for movie in movies:
                gather.say(f'{movie.movie_name}')

        vr.say('We did not receive your selection')
        vr.redirect(reverse('choose_movie'))

    return HttpResponse(str(vr), content_type='text/xml')


@csrf_exempt
def choose_schedule(request: HttpRequest) -> HttpResponse:
    vr = VoiceResponse()

    cinema = Cinema.objects.get(name=request.GET.get('cinema'))
    movie_name = request.POST.get('SpeechResult').strip('.')

    try:
        movie = Movie.objects.get(movie_name=movie_name)

    except Movie.DoesNotExist:
        vr.say('Movie was not found in the list!')
        vr.redirect(f'{reverse("choose_movie")}?cinema={cinema.name}')

    else:
        vr.say('Please select when you want to see the movie from the list.')
        cinema_name = cinema.name.replace(' ', '%20')
        movie_name = movie.movie_name.replace(' ', '%20')
        with vr.gather(
                action=f'{reverse("user_details")}?movie={movie_name}&cinema={cinema_name}',
                input='speech',
                timeout=3,
                speech_model='numbers_and_commands',
        ) as gather:
            gather.say('Please say the digit corresponding to the schedule time from the list:')
            schedules = list(
                Schedule.objects.filter(
                    cinema=cinema,
                    movie=movie,

                ))
            if len(schedules) == 0:
                gather.say('Sorry, the movie is not playing any time soon in this theater.')
            else:
                index = 1
                for schedule in schedules:
                    gather.say(
                        f'Say {index}, for seeing the movie at '
                        f'{schedule.time_slot} on {schedule.day} in room {schedule.room_id}')
                    index += 1

        vr.say('We did not receive your selection')
        vr.redirect(reverse('choose_schedule'))

    return HttpResponse(str(vr), content_type='text/xml')


@csrf_exempt
def user_details(request: HttpRequest) -> HttpResponse:

    movie = Movie.objects.get(movie_name=request.GET.get('movie'))
    cinema = Cinema.objects.get(name=request.GET.get('cinema'))

    id = request.POST.get('SpeechResult').strip('.')
    id = w2n.word_to_num(id)

    try:
        schedule = list(
            Schedule.objects.filter(
                cinema=cinema,
                movie=movie,
            ))[id]

    except Schedule.DoesNotExist:
        vr = VoiceResponse()
        vr.say('I did not get that. Please Repeat!')
        vr.redirect(f'{reverse("choose-schedule")}?cinema={schedule.cinema.id}')

    vr = VoiceResponse()
    vr.say('What is your name?')

    vr.gather(
            action=reverse("confirm_reservation"),
            input='speech',
            timeout=3,
            speech_model='numbers_and_commands')

    vr.say('I did not get that. Please repeat your name!')
    vr.redirect(reverse('user_details'))
    return HttpResponse(str(vr), content_type='text/xml')


@csrf_exempt
def make_reservation(request: HttpRequest) -> HttpResponse:
    vr = VoiceResponse()

    movie = Movie.objects.get(movie_name=request.GET.get('movie'))
    cinema = Cinema.objects.get(name=request.GET.get('cinema'))
    schedule = Schedule.objects.get(name=request.GET.get('schedule'))

    user_name = request.POST.get('SpeechResult').strip('.')

    vr.say('Do you confirm the reservation for the movie ' + movie.movie_name + ' on ' + schedule.day + ' in ' + cinema.name + ' for ' + user_name + ' ?')

    vr.gather(
        action=reverse('make_reservation'),
        input='speech',
        timeout=3,
        speech_model='numbers_and_commands', )

    vr.say('I did not get that! Please repeat!')
    vr.redirect(reverse('make_reservation'))

    return HttpResponse(str(vr), content_type='text/xml')

@csrf_exempt
def confirm_reservation(request: HttpRequest) -> HttpResponse:
    vr = VoiceResponse()

    confirmation = request.POST.get('SpeechResult').strip('.')
    if confirmation.lower() == 'yes':
        vr.say('Your reservation is complete! Thank you for using our movie reservation system!')
    else:
        vr.say('Thank you for your time call us again if you change your mind! Goodbye!')
    vr.hangup()

    return HttpResponse(str(vr), content_type='text/xml')

