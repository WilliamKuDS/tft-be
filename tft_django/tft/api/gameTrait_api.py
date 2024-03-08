import json
from django.http import HttpResponse
import tft.service.gameTrait_service as service


def createGameTrait(request):
    body = json.loads(request.body)
    data = service.createGameTrait(body)
    return HttpResponse(data)


def readGameTrait(request):
    body = json.loads(request.body)
    data = service.readGameTrait(body)
    return HttpResponse(data)


def updateGameTrait(request):
    body = json.loads(request.body)
    data = service.updateGameTrait(body)
    return HttpResponse(data)


def deleteGameTrait(request):
    body = json.loads(request.body)
    service.deleteGameTrait(body)
    return HttpResponse('Game Trait Deleted')
