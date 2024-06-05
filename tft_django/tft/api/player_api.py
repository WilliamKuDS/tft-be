import json
from django.http import HttpResponse
import tft.service.player_service as service


def createPlayer(request):
    body = json.loads(request.body)
    data = service.createPlayer(body)
    return HttpResponse(data)

def readPlayerByID(request):
    body = json.loads(request.body)
    data = service.readPlayerID(body)
    return HttpResponse(data)

def readPlayerByPUUID(request):
    puuid, region = request.headers["puuid"], request.headers["region"]
    status_code = service.updateOrCreatePlayerByPUUID(puuid, region)
    return HttpResponse(status=status_code)


def readPlayerByName(request):
    playerName = request.headers["playerName"]
    data = service.readPlayerValues(playerName)
    return HttpResponse(data)


def updatePlayer(request):
    body = json.loads(request.body)
    data = service.updatePlayer(body)
    return HttpResponse(data)


def deletePlayerByID(request):
    body = json.loads(request.body)
    service.deletePlayerID(body)
    return HttpResponse('Player Deleted')


def deletePlayerByValues(request):
    body = json.loads(request.body)
    service.deletePlayerValues(body)
    return HttpResponse('Player Deleted')
