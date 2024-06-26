import json
from django.http import HttpResponse, JsonResponse
import tft.service.item_service as service


def createItem(request):
    body = json.loads(request.body)
    data = service.createItem(body)
    return HttpResponse(data)


def readItem(request):
    body = json.loads(request.body)
    data = service.readItem(body)
    return HttpResponse(data)


def readItemAllByPatch(request):
    patch = request.GET.get('patch')
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 20)
    order_by = request.GET.get('order_by', 'id')
    data = service.readItemAllByPatch(patch, page, page_size, order_by)
    return JsonResponse(data)


def readItemAll(request):
    data = service.readItemAll()
    return HttpResponse(data)


def updateItem(request):
    body = json.loads(request.body)
    data = service.updateItem(body)
    return HttpResponse(data)


def deleteItem(request):
    body = json.loads(request.body)
    service.deleteItem(body)
    return HttpResponse('Item Deleted')
