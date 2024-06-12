import json
from django.http import HttpResponse
from django.http import JsonResponse
import tft.service.match_service as service


def createMatch(request):
    body = json.loads(request.body)
    data = service.createMatch(body)
    return HttpResponse(data)


def readMatch(request):
    puuid, region = request.headers['puuid'], request.headers['region']
    data = service.readMatch(puuid, region)
    return HttpResponse(data)


def updateMatch(request):
    body = json.loads(request.body)
    data = service.updateMatch(body)
    return HttpResponse(data)


def deleteMatch(request):
    body = json.loads(request.body)
    service.deleteMatch(body)
    return HttpResponse('Match Deleted')

def getBasicMatch(request):
    puuid, region = request.headers['puuid'], request.headers['region']
    cursor = request.GET.get('cursor', 0)
    match, next_cursor = service.getBasicMatch(puuid, region, cursor)

    data = {
        'results': match,
        'next': next_cursor,
    }

    return JsonResponse(data)

def getDetailedMatch(request):
    puuid, match_id = request.headers['puuid'], request.headers['matchID']
    data = service.getDetailedMatch(puuid, match_id)
    return HttpResponse(data)
