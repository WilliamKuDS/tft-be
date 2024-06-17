import json
from django.http import HttpResponse
import tft.service.trait_service as service


def createTrait(request):
    body = json.loads(request.body)
    data = service.createTrait(body)
    return HttpResponse(data)


def readTrait(request):
    body = json.loads(request.body)
    data = service.readTrait(body)
    return HttpResponse(data)


def readTraitAllByPatch(request):
    patch = request.headers['patch']
    data = service.readTraitAllByPatch(patch)
    return HttpResponse(data)


def updateTrait(request):
    body = json.loads(request.body)
    data = service.updateTrait(body)
    return HttpResponse(data)


def deleteTraitByID(request):
    body = json.loads(request.body)
    service.deleteTrait(body)
    return HttpResponse('Trait Deleted')

