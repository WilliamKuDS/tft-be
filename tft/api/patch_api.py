import json
from django.http import HttpResponse, JsonResponse
import tft.service.patch_service as service


def createPatch(request):
    body = json.loads(request.body)
    data = service.createPatch(body)
    return HttpResponse(data)


def readPatch(request):
    body = json.loads(request.body)
    data = service.readPatch(body)
    return HttpResponse(data)


def readPatchAll(request):
    data = service.readPatchAll()
    return JsonResponse(data, safe=False)


def updatePatch(request):
    body = json.loads(request.body)
    data = service.updatePatch(body)
    return HttpResponse(data)


def deletePatch(request):
    body = json.loads(request.body)
    service.deletePatch(body)
    return HttpResponse('Patch Deleted')
