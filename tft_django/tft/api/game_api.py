import json
from django.http import HttpResponse
import tft.service.game_service as service


def createGame(request):
    body = json.loads(request.body)
    data = service.createGame(body)
    return HttpResponse(data)


def readGameByID(request):
    body = json.loads(request.body)
    data = service.readGameByID(body)
    return HttpResponse(data)


def readGameByPlayerGame(request):
    body = json.loads(request.body)
    data = service.readGameByPlayerGame(body)
    return HttpResponse(data)


def updateGame(request):
    body = json.loads(request.body)
    data = service.updateGame(body)
    return HttpResponse(data)


def deleteGameByID(request):
    body = json.loads(request.body)
    service.deleteGameByID(body)
    return HttpResponse('Game Deleted')


def deleteGameByPlayerGame(request):
    body = json.loads(request.body)
    service.deleteGameByPlayerGame(body)
    return HttpResponse('Game Deleted')
