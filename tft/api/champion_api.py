import json
from django.http import HttpResponse
import tft.service.champion_service as service


def createChampion(request):
    body = json.loads(request.body)
    data = service.createUnit(body)
    return HttpResponse(data)


def readChampion(request):
    body = json.loads(request.body)
    data = service.readUnit(body)
    return HttpResponse(data)




def readChampionAll(request):
    data = service.readUnitAll()
    return HttpResponse(data)


def updateChampion(request):
    body = json.loads(request.body)
    data = service.updateUnit(body)
    return HttpResponse(data)


def deleteChampion(request):
    body = json.loads(request.body)
    service.deleteUnit(body)
    return HttpResponse('Unit Deleted')

