# Microsoft Engage 2022 Algorithm Demonstration By Vaibhav Gawad 
MovieFlex

##  ABOUT PROJECT
Using consine Similarity Between all Movies I am going to recommend user Movie based on the Movie he Watched in the past or he liked the most.

![image](https://user-images.githubusercontent.com/58821506/171170154-7fa5efd5-0572-47b4-a08f-9949ec75bd32.png)


User will get Movie Recommendation Based on the Content Based Filtering and Genre Based Filtering.

User can get Recommnendation of recommendations.

You can able to see Genres of all the movies.

Also can be able to get more information of movies from IMDB on clicking of Know more button of every movie card.

## Learnings
- Web Development Using Django 
- API Building
- Consuming Pythons libraries such as **Sklearns**, **numpy**, **pandas**, **surprise**
- Version Controlling using Git
- And Deployement of Project on Azure cloud.

#
**Video Demonstration** : https://youtu.be/6_EAMuwWctk
#
**Algorithm Walkthrough Explained in this Excel**  https://docs.google.com/spreadsheets/d/11AUtJWwsBh0lnXZyvuM5OW5qvQ5yovA1sd0_srtkAms/edit?usp=sharing

## Hosted here
- Azure Cloud : https://movieflex.azurewebsites.net/ , https://movieflexx.azurewebsites.net/
- Heroku : https://movieflexx.herokuapp.com/

## Tech Stack 
- Python
- Django
- Html 
- Css
- Javascript
- Tailwind Css
- Scikit-Learn 
- Jypyter Notebook

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/vaibhav31s/moviesystem
$ cd moviesystem
```
Download Files From Mega and put it into MovieSystem folder
https://mega.nz/folder/wewSyK6Y#Bav2h7unGv670zAcNpIKwQ

Then install the dependencies:
```sh
$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

If Static files didnt load please change  #``` DEBUG = True ``` it is  in ```  ./moviesystem/settings.py ``` 

## Output
                                                              `` Index page ``
![movieflex azurewebsites net_](https://user-images.githubusercontent.com/58821506/171163493-ef5ef767-c76d-4fc8-9f69-97207812051c.png)
                                                              `` Recommendations page ``
![movieflex azurewebsites net_recommendations](https://user-images.githubusercontent.com/58821506/171162484-3b4785a1-79bc-4595-81a2-3d00ae10c641.png)
                                                              `` Genre Based Recommendations ``
![movieflex azurewebsites net_genre](https://user-images.githubusercontent.com/58821506/171163026-79ea5147-e5de-4bc8-b262-aaef05416f36.png)






