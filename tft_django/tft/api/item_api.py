import json
from django.http import HttpResponse
import tft.service.item_service as service


def createItem(request):
    body = json.loads(request.body)
    data = service.createItem(body)
    return HttpResponse(data)


def readItemByID(request):
    body = json.loads(request.body)
    data = service.readItemID(body)
    return HttpResponse(data)


def readItemByName(request):
    body = json.loads(request.body)
    data = service.readItemName(body)
    return HttpResponse(data)


def readItemAll(request):
    data = service.readItemAll()
    return HttpResponse(data)


def updateItem(request):
    body = json.loads(request.body)
    data = service.updateItem(body)
    return HttpResponse(data)


def deleteItemByID(request):
    body = json.loads(request.body)
    service.deleteItemID(body)
    return HttpResponse('Item Deleted')


def deleteItemByName(request):
    body = json.loads(request.body)
    service.deleteItemName(body)
    return HttpResponse('Item Deleted')
