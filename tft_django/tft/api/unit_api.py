import json
from django.http import HttpResponse
import tft.service.unit_service as service


def createUnit(request):
    body = json.loads(request.body)
    data = service.createUnit(body)
    return HttpResponse(data)


def readUnitByID(request):
    body = json.loads(request.body)
    data = service.readUnitID(body)
    return HttpResponse(data)


def readUnitByName(request):
    body = json.loads(request.body)
    data = service.readUnitName(body)
    return HttpResponse(data)


def updateUnit(request):
    body = json.loads(request.body)
    data = service.updateUnit(body)
    return HttpResponse(data)


def deleteUnitByID(request):
    body = json.loads(request.body)
    service.deleteUnitID(body)
    return HttpResponse('Unit Deleted')


def deleteUnitByName(request):
    body = json.loads(request.body)
    service.deleteUnitName(body)
    return HttpResponse('Unit Deleted')
