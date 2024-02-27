from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:region>/", views.region, name="region"),
    path("<str:region>/<str:name>/", views.name, name="name"),
    path("game", views.game, name="game")
    #path("game/all", views.get_all_games, name="get_all_games")
]
