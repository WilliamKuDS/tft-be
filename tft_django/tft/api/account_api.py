import json
from django.http import HttpResponse
import tft.service.account_service as service


def createAccount(request):
    body = json.loads(request.body)
    data = service.createPlayer(body)
    return HttpResponse(data)


def readAccount(request):
    account_data = {'puuid': request.headers['puuid'], 'gameName': request.headers['gameName'],
                    'tagLine': request.headers['tagLine']}
    status_code = service.readPlayer(account_data)
    return HttpResponse(status=status_code)


def updateAccount(request):
    playerNameRegion = request.headers["playerNameRegion"]
    service_code = service.updatePlayer(playerNameRegion)
    return HttpResponse(status=service_code)


def deleteAccount(request):
    body = json.loads(request.body)
    service.deletePlayerValues(body)
    return HttpResponse('Player Deleted')

def createUpdateAccount(request):
    account_data = {'puuid': request.headers['puuid'], 'gameName': request.headers['gameName'],
                    'tagLine': request.headers['tagLine']}
    status_code = service.createUpdateAccount(account_data)
    return HttpResponse(status=status_code)
