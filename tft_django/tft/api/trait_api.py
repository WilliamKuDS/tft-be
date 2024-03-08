import json
from django.http import HttpResponse
import tft.service.trait_service as service


def createTrait(request):
    body = json.loads(request.body)
    data = service.createTrait(body)
    return HttpResponse(data)


def readTraitByID(request):
    body = json.loads(request.body)
    data = service.readTraitID(body)
    return HttpResponse(data)


def readTraitByName(request):
    body = json.loads(request.body)
    data = service.readTraitName(body)
    return HttpResponse(data)


def updateTrait(request):
    body = json.loads(request.body)
    data = service.updateTrait(body)
    return HttpResponse(data)


def deleteTraitByID(request):
    body = json.loads(request.body)
    service.deleteTraitID(body)
    return HttpResponse('Trait Deleted')


def deleteTraitByName(request):
    body = json.loads(request.body)
    service.deleteTraitName(body)
    return HttpResponse('Trait Deleted')
