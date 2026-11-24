from django.urls import path

from trial import views

urlpatterns = [
    path("", views.index, name="Homepage"),
    path("recommendations", views.recommendations, name="recommendations"),
    path("recommendations/", views.recommendations),
    path("genre", views.genre, name="genre"),
    path("genre/", views.genre),
    path("movieflix", views.movieflix, name="movieflix"),
    # JSON API (the old /product/ endpoints)
    path("product/", views.titles, name="product"),
    path("product/<id>", views.product_details, name="product_details"),
    path("api/titles", views.titles, name="titles"),
]
