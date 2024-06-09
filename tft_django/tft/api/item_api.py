import json
from django.http import HttpResponse
import tft.service.item_service as service


def createItem(request):
    body = json.loads(request.body)
    data = service.createItem(body)
    return HttpResponse(data)


def readItem(request):
    body = json.loads(request.body)
    data = service.readItem(body)
    return HttpResponse(data)



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

