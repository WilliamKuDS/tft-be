from django.shortcuts import render
from .models import User
from .models import Game
from .misc import saveJSONToDatabase
import json
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize

def index(request):
    return HttpResponse("Hello, world. You're at the tft_django")

@csrf_exempt
def saveOneGame(request: str):
    if request.method == 'GET':
        games = Game.objects.all()
        lst =[]
        for game in games:
            lst.append(game.traits)
        return HttpResponse(games)

    if request.method == 'POST':
        data = json.loads(request)
        saveJSONToDatabase(data)
        return HttpResponse('Done')

@csrf_exempt
def deleteAllGames(request):
    if request.method == 'DELETE':
        Game.objects.all().delete()
    return HttpResponse('Purged')

@csrf_exempt
def getGames(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        playerName = body['playerName']
        playerGames = Game.objects.filter(playerName=playerName)
    return JsonResponse([game.serialize() for game in playerGames], safe=False)





