import json
from django.http import HttpResponse
import tft.service.match_service as service


def createMatch(request):
    body = json.loads(request.body)
    data = service.createGame(body)
    return HttpResponse(data)

def readMatch(request):
    body = json.loads(request.body)
    data = service.createGame(body)
    return HttpResponse(data)



def updateMatch(request):
    body = json.loads(request.body)
    data = service.updateGame(body)
    return HttpResponse(data)


def deleteMatch(request):
    body = json.loads(request.body)
    service.deleteGameByID(body)
    return HttpResponse('Game Deleted')

