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


def readPlayerByValues(request):
    body = json.loads(request.body)
    data = service.readPlayerValues(body)
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
