from django.shortcuts import render
# from .misc import saveJSONToDatabase
import json
# Create your api here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

from .models import player
from .models import game_info

def index(request):
    return HttpResponse("You're at the tft_django API. If you are here, you don't know what you are doing.")

def createPlayer(request):
    pass

@csrf_exempt
def readPlayer(request):
    body = json.loads(request.body)
    name = str(body["player_name"])
    region = str(body["player_region"]).lower()
    #queue = str(body["game_queue"]).lower()

    playerID = player.objects.get(player_name=name, region=region)
    playerGames = game_info.objects.filter(player_id=playerID)
    print(len(playerGames))
    requests_per_page = request.GET.get('requests')
    page_number = request.GET.get("page")
    paginator = Paginator(playerGames, requests_per_page)
    paginator_playerGames = paginator.get_page(page_number)
    return JsonResponse([[model_to_dict(game) for game in paginator_playerGames]], safe=False)

def updatePlayer(request):
    pass

def deletePlayer(request):
    pass

def createGame(request):
    pass

def readGame(request):
    pass

def updateGame(request):
    pass

def deleteGame(request):
    pass

# @csrf_exempt
# def saveOneGame(request: str):
#     if request.method == 'GET':
#         games = Game.objects.all()
#         lst =[]
#         for game in games:
#             lst.append(game.traits)
#         return HttpResponse(games)
#
#     if request.method == 'POST':
#         data = json.loads(request)
#         saveJSONToDatabase(data)
#         return HttpResponse('Done')
#
# @csrf_exempt
# def deleteAllGames(request):
#     if request.method == 'DELETE':
#         Game.objects.all().delete()
#     return HttpResponse('Purged')
#
# @csrf_exempt
# def getGames(request):
#     if request.method == 'POST':
#         body = json.loads(request.body.decode('utf-8'))
#         playerName = body['playerName']
#         playerGames = Game.objects.filter(playerName=playerName)
#     return JsonResponse([game.serialize() for game in playerGames], safe=False)
#
#



