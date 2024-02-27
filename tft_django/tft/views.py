from django.shortcuts import render
from .models import User
from .models import Game
import json

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("Hello, world. You're at the tft_django")

def region(request, region):
    return HttpResponse("Current Region is %s" % region)
@csrf_exempt
def game(request):
    if request.method == 'GET':
        games = Game.objects.all()
        lst =[]
        for game in games:
            lst.append(game.traits)
        return HttpResponse(games)

    if request.method == 'POST':
        body = json.load(request)
        game_instance = Game.objects.create(
            gameID = body["GameID"],
            queue = body["Queue"],
            placement = body["Placement"],
            level = body["Level"],
            length = body["Length"],
            round = body["Round"],
            augments = body["Augments"],
            headliner = body["Headliner"],
            traits = body["Traits"],
            units = body["Units"]
        )
        game_instance.save()
        return HttpResponse('Done')

#Get all games
@csrf_exempt
def get_all_games(request):
    if request.method == "GET":
        games = Game.objects.all()
        return HttpResponse(games)

def name(request, name, region):
    try:
        get_name = str(User.objects.get(name=name, region=region))
        split_name = get_name.split('/')
        # get_region = User.objects.get(region=region)
        return HttpResponse("Current Name is {}-{}, Region: {}".format(split_name[0], split_name[1], split_name[2]))
    except:
        return HttpResponse("No User Found")



