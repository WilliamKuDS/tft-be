import json
from django.http import HttpResponse
import tft.service.patch_service as service


def createPatch(request):
    body = json.loads(request.body)
    data = service.createPatch(body)
    return HttpResponse(data)


def readPatchByID(request):
    body = json.loads(request.body)
    data = service.readPatchID(body)
    return HttpResponse(data)


def readPatchBySetID(request):
    body = json.loads(request.body)
    data = service.readPatchPatchID(body)
    return HttpResponse(data)


def updatePatch(request):
    body = json.loads(request.body)
    data = service.updatePatch(body)
    return HttpResponse(data)


def deletePatchByID(request):
    body = json.loads(request.body)
    service.deletePatch(body)
    return HttpResponse('Patch Deleted')
