from copyreg import pickle
import imp
from multiprocessing import context
import pkgutil
from django.shortcuts import render
from django.http import HttpResponse
import requests

import template
import numpy as np
import pandas as pd
import pickle
import os
import csv
from rest_framework.decorators import api_view
from rest_framework.response import Response
movies_list=pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_list)
type(movies_list)
# print(movies)
# with open('movies.pkl','rb') as file:
#     employee = pickle.load(file)

# print(movies_list)  
# movies= pd.read_csv('../../static/tmdb_5000_movies.csv')
# credits = pd.read_csv('../../static/tmdb_5000_credits.csv')

# Create your views here.
@api_view()
def product_list(request):
    context = {
                "passwords":movies['title'].values,
            }  
    return Response(context)
@api_view()
def product_details(request,id):
 
    return Response(id)
    


def index(request):
    context = {
                "passwords":movies['title'].values,
            }  
    return render(request, 'index.html', context)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d5d568d260d85ea19b7153923c213fe9&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:5]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

def recommendations(request):

    if "movie_name" in request.POST:
        name = request.POST.get('name')
        # vaibhav = recommend(name)
        # print(vaibhav)
        recommended_movie_names,recommended_movie_posters = recommend(name)
        mylist = zip(recommended_movie_names, recommended_movie_posters)
        print(mylist)
    context={ 'mylist': mylist}
    return render(request,'recomendations.html',context)

def movieflix(request):
    context = {
                "passwords":'s',
            }  
    return render(request, 'movieFlix.html', context)