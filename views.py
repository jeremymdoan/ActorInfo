from django.shortcuts import get_object_or_404, get_list_or_404, render, render_to_response
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic

from actors.models import Actor, Movies

def home(request):
    actors_stats_1 = Movies.special_objects.actors_stats_1()
    actors_stats_2 = Movies.special_objects.actors_stats_2()
    return render_to_response('actors/home.html', {'actors_stats_1': actors_stats_1, 'actors_stats_2': actors_stats_2})

def details(request, actor_id):
    num_films = Movies.special_objects.movies_amount(actor_id)
    year_range = num_films[-1][0] - num_films[0][0]
    ratings = Movies.special_objects.movies_ratings(actor_id)
    actor = get_object_or_404(Actor, pk=actor_id)
    avg_ratings = []
    for row in ratings:
        avg_ratings.append(float(row[1]))
    avg_film = []
    for row in num_films:
        avg_film.append(float(row[1]))
    avg_ratings = sum(avg_ratings)/float(len(avg_ratings))
    avg_film = sum(avg_film)/float(len(num_films))
    avg_ratings, avg_film = round(avg_ratings, 2), round(avg_film, 2)
    stats = (avg_ratings, ratings[0][0], len(ratings), year_range, avg_film) 
    return render(request, 'actors/details.html', {'movies_amount': num_films, 'actors': actor, 'movies_ratings': ratings, 'movies_stats':stats})

def search(request):
    selected_choice = request.GET['actor_name']
    #try:
    #    prim_key = Actor.objects.get(actor=selected_choice).pk
    #except (KeyError, Actor.DoesNotExist):
    #    return render(request, 'actors/home.html', {'error_message': 'Sorry, that actor is not available.'})
    actors = Actor.objects.filter(actor__icontains=selected_choice)
    if not actors.exists():
	return render(request, 'actors/search.html', {'error_message': 'Sorry, there are no actors that match your search. Please try again.'})
    else:
        return render(request, 'actors/search.html', {'actors': actors})

# Create your views here.
