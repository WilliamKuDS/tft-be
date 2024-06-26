import json
from django.http import HttpResponse, JsonResponse
import tft.service.augment_service as service


def createAugment(request):
    body = json.loads(request.body)
    data = service.createAugment(body)
    return HttpResponse(data)


def readAugment(request):
    body = json.loads(request.body)
    data = service.readAugment(body)
    return HttpResponse(data)


def readAugmentAllByPatch(request):
    patch = request.GET.get('patch')
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 20)
    order_by = request.GET.get('order_by', 'id')
    data = service.readAugmentAllByPatch(patch, page, page_size, order_by)
    return JsonResponse(data)


def updateAugment(request):
    body = json.loads(request.body)
    data = service.updateAugment(body)
    return HttpResponse(data)


def deleteAugment(request):
    body = json.loads(request.body)
    service.deleteAugment(body)
    return HttpResponse('Augment Deleted')
