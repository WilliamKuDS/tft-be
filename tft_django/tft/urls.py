from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #path("<str:region>/", views.region, name="region"),
    #path("<str:region>/<str:name>/", views.name, name="name"),
    path("game", views.saveOneGame, name="game"),
    path("deleteall", views.deleteAllGames, name="deleteall"),
    path("game/get", views.getGames, name="getGame")
    #path("game/all", views.get_all_games, name="get_all_games")
]
