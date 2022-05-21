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
                "movies":movies['title'].values,
            }  
    return render(request, 'index1.html', context)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d5d568d260d85ea19b7153923c213fe9&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def fetch_rating(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d5d568d260d85ea19b7153923c213fe9&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    return "9.4"

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

def movieInfo(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[0:1]:
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
        recommended_movie_name,recommended_movie_poster = movieInfo(name)
        rating = fetch_rating(name)
        mylist = zip(recommended_movie_names, recommended_movie_posters)
        mylist1 = zip(recommended_movie_name, recommended_movie_poster,rating)
        print(mylist1)
        print(mylist)
    context={ 'mylist': mylist,'mylist2':mylist1}
    return render(request,'recomendations.html',context)


def topMovies():
    url ="https://api.themoviedb.org/3/movie/top_rated?api_key=d5d568d260d85ea19b7153923c213fe9&language=en-US&page=1"
    data = requests.get(url)
    data = data.json()
    
    list1 = []
    list2 = []
    for i in range(0,10):
        list1.append(data['results'][i]['original_title'])
        poster_path = data['results'][i]['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        list2.append(full_path)
      
   
    print(list1)
    print(list2)
    print(type(list1))
    return list1,list2

def movieflix(request):
    recommended_movie_names,recommended_movie_posters =  topMovies()
    mylist = zip(recommended_movie_names, recommended_movie_posters)
    context = {
                "top":mylist,
            }  
    return render(request, 'index1.html', context)