from django.shortcuts import render
from django.http import HttpResponse

import ast
import csv
import json

from myapp.models import BaconNumber

def index(request):
	response = json.dumps([{'abc' : 'def'}])
	return HttpResponse(response, content_type='text/json')

def populateDegree(setOfMovies, actorMovies, movieActors, remainingActors, remainingMovies, currentDegree):
	if not (setOfMovies and remainingMovies):
		return
	# print(f"starting level {currentDegree} with movies {setOfMovies}")
	current_degree_actors = []
	for movie in setOfMovies:
		remainingMovies.remove(movie)
		for actor in movieActors[movie]:
			if actor in remainingActors:
				remainingActors.remove(actor)
				current_degree_actors.append(actor)
	# print(f"list of actors: {current_degree_actors}")
	setOfNextDegreeMovies = set()
	for actor in current_degree_actors:
		# 	actorMovieMapping = ActorMovieMapping(actorID=actor, movieID=movie)
		actorDegree = BaconNumber(name = actor, baconNumber = currentDegree)
		actorDegree.save()
		# print(f"actor {actor} is degree {currentDegree}")
		for movie in actorMovies[actor]:
			if movie in remainingMovies:
				setOfNextDegreeMovies.add(movie)

	populateDegree(setOfNextDegreeMovies, actorMovies, movieActors, remainingActors, remainingMovies, currentDegree + 1)

def preprocess(request):
	BaconNumber.objects.all().delete()
	
	with open('movie_data/credits.csv', newline='') as csv_file:
		kevin_bacon_movies = set()
		actor_dict = {} # name => (movieIDs)
		movie_dict = {} # id => (actorNames)
		actorSet = set()
		movieSet = set()
		credits_reader = csv.reader(csv_file, delimiter=',')
		for lineno, credits in enumerate(credits_reader):
			cast_info = ast.literal_eval(credits[0])
			movie_id = credits[2]
			# print(f"adding movie: # {lineno} which is movie id {movie_id}")
			movie_dict[movie_id] = []
			movieSet.add(movie_id)
			for cast in cast_info:
				actor_name = cast["name"]
				if actor_name == "Kevin Bacon":
					kevin_bacon_movies.add(movie_id)
				else:
					movie_dict[movie_id].append(actor_name)
					if not actor_dict.get(actor_name):
						actor_dict[actor_name] = [movie_id]
						actorSet.add(actor_name)
					else:
						actor_dict[actor_name].append(movie_id)

	kevinBacon = BaconNumber(name = "Kevin Bacon", baconNumber = 0)
	kevinBacon.save()
	populateDegree(kevin_bacon_movies, actor_dict, movie_dict, actorSet, movieSet, 1)
	response = json.dumps([{'abc' : 'defg'}])
	return HttpResponse(response, content_type='text/json')

def getDegree(request, actor_name):
	if request.method == 'GET':
		try:
			actor = BaconNumber.objects.get(name=actor_name)
			response = json.dumps([{f'Kevin Bacon Number for actor {actor_name}' : f'{actor.baconNumber}'}])
		except:
			response = json.dumps([{'Error': 'No actor with that name'}])
		return HttpResponse(response, content_type='text/json')
