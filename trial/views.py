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
  
def movieInfo(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    generes=[]
    for i in distances[0:1]:
        # fetch the mov ie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        generes.append(movies.iloc[i[0]].genres)
    
    return recommended_movie_names,recommended_movie_posters,generes



genres = {
      28: "Action",
      12: "Animation",
      16: "Animation",
      35: "Comedy",
      28: "Action",
      80: "Crime", 
      99: "Documentary",
      18: "Drama", 
      10751: "Family",
      14: "Fantasy",
      36: "History",
      27: "Horror",
      10402: "Music",
      9648: "Mystery",
      10749: "Romance",
      878: "Science Fiction", 
      10770: "TV Movie",
      53: "Thriller", 
      10752: "War",
      37: "Western",

    }

def fetch_genres(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d5d568d260d85ea19b7153923c213fe9&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
  
    
    print(data['genres'])
    return geners
  
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    generes=[]
    rating=[]
    counter=0
    for i in distances[1:10]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        generes.append(movies.iloc[i[0]].genres)
        # rating = movies.iloc[i[0]].vote_average
        counter+=1
    print(rating)
    return recommended_movie_names,recommended_movie_posters,generes

def topMovies():
    url ="https://api.themoviedb.org/3/movie/top_rated?api_key=d5d568d260d85ea19b7153923c213fe9&language=en-US&page=1"
    data = requests.get(url)
    data = data.json()
    
    title = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = [[],[],[],[],[],[],[],[],[],[]]
    for i in range(0,8):
        title.append(data['results'][i]['title'])
        list3.append(data['results'][i]['vote_average'])
        list4.append(data['results'][i]['overview'])
        list5.append(data['results'][i]['id'])
        for j in data['results'][i]['genre_ids']:
            list6[i].append(genres[j])
        poster_path = data['results'][i]['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        list2.append(full_path)
        
    return title,list2,list3,list4,list5,list6

def recommendations(request):

    if "movie_name" in request.POST:
        name = request.POST.get('name')
        # vaibhav = recommend(name)
        # print(vaibhav)
        recommended_movie_names,recommended_movie_posters,generes = recommend(name)
        recommended_movie_name,recommended_movie_poster, genres1= movieInfo(name)
        
        mylist = zip(recommended_movie_names, recommended_movie_posters,generes)
        mylist1 = zip(recommended_movie_name, recommended_movie_poster,genres1)
     
    context={ 'mylist': mylist,'mylist2':mylist1}
    return render(request,'recomendations.html',context)

def movieflix(request):
    recommended_movie_names,recommended_movie_posters, ratings, overview,id,genre =  topMovies()
    mylist = zip(recommended_movie_names,recommended_movie_posters,ratings,overview,id,genre)
    context = {
                "top":mylist,
            }  
    return render(request, 'cardsTesting.html', context)

def index(request):
    recommended_movie_names,recommended_movie_posters, ratings, overview,id,genre =  topMovies()
    mylist = zip(recommended_movie_names,recommended_movie_posters,ratings,overview,id,genre)
    context = {
                "movies":movies['title'].values,"top":mylist,
            }  
    return render(request, 'index1.html', context)
