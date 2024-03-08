import json
from django.http import HttpResponse
import tft.service.augment_service as service


def createAugment(request):
    body = json.loads(request.body)
    data = service.createAugment(body)
    return HttpResponse(data)


def readAugmentByID(request):
    body = json.loads(request.body)
    data = service.readAugmentID(body)
    return HttpResponse(data)


def readAugmentByName(request):
    body = json.loads(request.body)
    data = service.readAugmentName(body)
    return HttpResponse(data)


def updateAugment(request):
    body = json.loads(request.body)
    data = service.updateAugment(body)
    return HttpResponse(data)


def deleteAugmentByID(request):
    body = json.loads(request.body)
    service.deleteAugmentID(body)
    return HttpResponse('Augment Deleted')


def deleteAugmentByName(request):
    body = json.loads(request.body)
    service.deleteAugmentName(body)
    return HttpResponse('Augment Deleted')
