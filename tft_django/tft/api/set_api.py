import json
from django.http import HttpResponse
import tft.service.set_service as service


def createSet(request):
    body = json.loads(request.body)
    data = service.createSet(body)
    return HttpResponse(data)


def readSetByID(request):
    body = json.loads(request.body)
    data = service.readSetID(body)
    return HttpResponse(data)


def readSetByName(request):
    body = json.loads(request.body)
    data = service.readSetName(body)
    return HttpResponse(data)


def updateSet(request):
    body = json.loads(request.body)
    data = service.updateSet(body)
    return HttpResponse(data)


def deleteSetByID(request):
    body = json.loads(request.body)
    service.deleteSet(body)
    return HttpResponse('Set Deleted')
