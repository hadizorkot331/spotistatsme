from django.urls import path
from . import views

app_name = "stats"
urlpatterns = [
    path("index", views.index, name="index"),
    path("recents", views.recents, name="recents"),
    path("fav_artists", views.fav_artists, name="fav_artists"),
]
