from django.urls import path

from . import views

urlpatterns = [
    path("user", views.queryUser, name="queryUser"),
    path("json", views.saveUser, name='saveUser'),
    path("fe", views.frontEndUser, name='frontEndUser'),
    path("subuser", views.querySubUsers, name='querySubUsers'),
    path("saveall", views.saveAllPlayers, name="saveall"),
    path("subsaveall", views.querySubPlayersAndSavePlayers, name="querySubPlayersAndSavePlayers"),
    path("update", views.updateUsers, name='updateUsers')
]