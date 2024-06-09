import json
from django.http import HttpResponse
import tft.service.summoner_service as service


def createSummoner(request):
    body = json.loads(request.body)
    data = service.createSummoner(body)
    return HttpResponse(data)


def readSummoner(request):
    puuid, region = request.headers['puuid'], request.headers['region']
    data = service.readSummoner(puuid, region)
    return HttpResponse(data)



def updateSummoner(request):
    playerNameRegion = request.headers["playerNameRegion"]
    service_code = service.updateSummoner(playerNameRegion)
    return HttpResponse(status=service_code)


def deleteSummoner(request):
    body = json.loads(request.body)
    service.deleteSummoner(body)
    return HttpResponse('Summoner Deleted')

def createUpdateSummoner(request):
    account_data = {'puuid': request.headers['puuid'], 'gameName': request.headers['gameName'],
                    'tagLine': request.headers['tagLine']}
    status_code = service.readPlayer(account_data)
    return HttpResponse(status=status_code)


