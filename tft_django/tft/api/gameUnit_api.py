import json
from django.http import HttpResponse
import tft.service.gameUnit_service as service


def createGameUnit(request):
    body = json.loads(request.body)
    data = service.createGameUnit(body)
    return HttpResponse(data)


def readGameUnit(request):
    body = json.loads(request.body)
    data = service.readGameUnit(body)
    return HttpResponse(data)


def updateGameUnit(request):
    body = json.loads(request.body)
    data = service.updateGameUnit(body)
    return HttpResponse(data)


def deleteGameUnit(request):
    body = json.loads(request.body)
    service.deleteGameUnit(body)
    return HttpResponse('Game Unit Deleted')
