import json
from django.http import HttpResponse
import tft.service.set_service as service


def createSet(request):
    body = json.loads(request.body)
    data = service.createSet(body)
    return HttpResponse(data)


def readSet(request):
    body = json.loads(request.body)
    data = service.readSet(body)
    return HttpResponse(data)


def updateSet(request):
    body = json.loads(request.body)
    data = service.updateSet(body)
    return HttpResponse(data)


def deleteSetByID(request):
    body = json.loads(request.body)
    service.deleteSet(body)
    return HttpResponse('Set Deleted')
