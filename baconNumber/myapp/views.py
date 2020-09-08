from django.shortcuts import render
from django.http import HttpResponse

import ast
import csv
import json
import gzip

from myapp.models import BaconNumber

# initial index screen
def index(request):
	response = json.dumps([{'URL to compute the Bacon Number of all actors' : '/preprocess'}, {'URL to query the Bacon Number of an actor' : '/getBaconNumber/<str:actor_name>'}])
	return HttpResponse(response, content_type='text/json')

# Recursively takes every connected actor and saves into SQLite3 DB entries the actor & his/her respective bacon number
def calculateBaconNumber(setOfMovies, actorMovies, movieActors, remainingActors, remainingMovies, currentBaconNumber):
	if not (setOfMovies and remainingMovies):
		return

	new_actors = []
	# Compile a list of new actors from the given set of movies
	for movie in setOfMovies:
		remainingMovies.remove(movie)
		for actor in movieActors[movie]:
			if actor in remainingActors:
				remainingActors.remove(actor)
				new_actors.append(actor)

	# Save the new actors & their bacon number + compile a list of new movies of the new actors.
	set_of_new_movies = set()
	for actor in new_actors:
		actorDegree = BaconNumber(name = actor, baconNumber = currentBaconNumber)
		actorDegree.save()
		for movie in actorMovies[actor]:
			if movie in remainingMovies:
				set_of_new_movies.add(movie)

	calculateBaconNumber(set_of_new_movies, actorMovies, movieActors, remainingActors, remainingMovies, currentBaconNumber + 1)

# preprocesses the data into dictionaries/sets for population.
def preprocess(request):
	BaconNumber.objects.all().delete()
	
	# Read gzipped file
	with gzip.open('movie_data/credits.csv.gz', mode="rt") as csv_file:
		kevin_bacon_movies = set()
		actor_dict = {}
		movie_dict = {}
		actor_set = set()
		movie_set = set()
		credits_reader = csv.reader(csv_file, delimiter=',')
		for lineno, credits in enumerate(credits_reader):
			cast_info = ast.literal_eval(credits[0])
			movie_id = credits[2]
			movie_dict[movie_id] = []
			movie_set.add(movie_id)
			for cast in cast_info:
				actor_name = cast["name"]
				if actor_name == "Kevin Bacon":
					kevin_bacon_movies.add(movie_id)
				else:
					movie_dict[movie_id].append(actor_name)
					if not actor_dict.get(actor_name):
						actor_dict[actor_name] = [movie_id]
						actor_set.add(actor_name)
					else:
						actor_dict[actor_name].append(movie_id)

	# Save the initial Kevin Bacon
	kevin_bacon = BaconNumber(name = "Kevin Bacon", baconNumber = 0)
	kevin_bacon.save()
	calculateBaconNumber(kevin_bacon_movies, actor_dict, movie_dict, actor_set, movie_set, 1)
	response = json.dumps([{'Preprocessing' : 'complete'}])
	return HttpResponse(response, content_type='text/json')

# Function to return the Bacon Number of the actor specified
def getBaconNumber(request, actor_name):
	if request.method == 'GET':
		try:
			actor = BaconNumber.objects.get(name=actor_name)
			response = json.dumps([{f'Kevin Bacon Number for actor {actor_name}' : f'{actor.baconNumber}'}])
		except:
			response = json.dumps([{'Error': 'No actor with that name'}])
		return HttpResponse(response, content_type='text/json')
