import json
from django.http import HttpResponse, JsonResponse
import tft.service.champion_service as service


def createChampion(request):
    body = json.loads(request.body)
    data = service.createUnit(body)
    return HttpResponse(data)


def readChampion(request):
    body = json.loads(request.body)
    data = service.readUnit(body)
    return HttpResponse(data)


def readChampionAllByPatch(request):
    patch = request.GET.get('patch')
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 20)
    order_by = request.GET.get('order_by', 'id')
    data = service.readChampionAllByPatch(patch, page, page_size, order_by)
    return JsonResponse(data)


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
