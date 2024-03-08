import json

from django.http import HttpResponse

import tft.service.gameInfo_service as service


def createGameInfo(request):
    body = json.loads(request.body)
    data = service.createGameInfo(body)
    return HttpResponse(data)


def readGameInfoByGameID(request):
    body = json.loads(request.body)
    data = service.readGameInfoGameID(body)
    return HttpResponse(data)


def readGameInfoByPlayerID(request):
    body = json.loads(request.body)
    data = service.readGameInfoPlayerID(body)
    return HttpResponse(data)


def updateGameInfo(request):
    body = json.loads(request.body)
    data = service.updateGameInfo(body)
    return HttpResponse(data)


def deleteGameInfoByGameID(request):
    body = json.loads(request.body)
    service.deleteGameInfoGameID(body)
    return HttpResponse('Game Deleted')
