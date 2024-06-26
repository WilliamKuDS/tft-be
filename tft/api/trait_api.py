import json
from django.http import HttpResponse, JsonResponse
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
    patch = request.GET.get('patch')
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 20)
    order_by = request.GET.get('order_by', 'id')
    data = service.readTraitAllByPatch(patch, page, page_size, order_by)
    return JsonResponse(data)


def updateTrait(request):
    body = json.loads(request.body)
    data = service.updateTrait(body)
    return HttpResponse(data)


def deleteTraitByID(request):
    body = json.loads(request.body)
    service.deleteTrait(body)
    return HttpResponse('Trait Deleted')

