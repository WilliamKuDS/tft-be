import json
from django.http import HttpResponse
import tft.service.augment_service as service


def createAugment(request):
    body = json.loads(request.body)
    data = service.createAugment(body)
    return HttpResponse(data)


def readAugment(request):
    body = json.loads(request.body)
    data = service.readAugment(body)
    return HttpResponse(data)



def updateAugment(request):
    body = json.loads(request.body)
    data = service.updateAugment(body)
    return HttpResponse(data)


def deleteAugment(request):
    body = json.loads(request.body)
    service.deleteAugment(body)
    return HttpResponse('Augment Deleted')

