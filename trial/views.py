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
    r = requests.get('http://127.0.0.1:8000/product/')
    
    context = {
                "passwords":movies['title'].values,
            }  
    return render(request, 'index.html', context)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list =sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:10]

    recommend_movies=[]
    for i in movies_list:
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies

def recommendations(request):
    if "movie_name" in request.POST:
        name = request.POST.get('name')
        vaibhav = recommend(name)
        print(vaibhav)
    context={'movies':vaibhav}
    return render(request,'recomendations.html',context)