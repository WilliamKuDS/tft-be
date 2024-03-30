from tft_selenium.tft_selenium import tftQuery
from tft_selenium.tft_selenium import getURL
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from tft import misc
from .misc import saveAllPlayersInFolder

# Create your api here.
@csrf_exempt
def queryUser(request):
    if request.method == 'POST':
        body = json.load(request)
        url = getURL(body['Name'], body['Region'].lower(), body['Tag'])
        player = tftQuery(body['Length'])
        player.getInfo(url)
        return HttpResponse('Got Player!')

@csrf_exempt
def saveUser(request):
    if request.method == 'GET':
        player = request.GET.get('file')
        path = os.getcwd() + '/tft_selenium/data/players/' + player
        with open(path, 'r') as data:
            for jsonLine in data.readlines()[1:]:
                misc.saveJSONToDatabase(json.loads(jsonLine))
    return HttpResponse(('Player Done: ' + str(player)))

@csrf_exempt
def frontEndUser(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        url = getURL(body['playerName'], body['playerRegion'].lower(), body['playerTag'])
        player = tftQuery()
        player.getInfo(url)

        path = os.getcwd() + '/tft_selenium/data/players/' + body['playerName'] + '-' + body['playerTag'] + '.json'
        with open(path, 'r') as data:
            for jsonLine in data.readlines()[1:]:
                misc.saveJSONToDatabase(json.loads(jsonLine))
    return HttpResponse("Its done suck it")

def updateUsers(request):
    if request.method == 'GET':
        numOfMatches = int(request.GET.get('numOfMatches'))
        tft = tftQuery(numOfMatches)
        tft.updatePlayers()
        saveAllPlayersInFolder()
    return HttpResponse('Updated Users and Saved')

def querySubUsers(request):
    if request.method == 'GET':
        numOfPlayers = int(request.GET.get('numOfPlayers'))
        numOfMatches = int(request.GET.get('numOfMatches'))
        player = tftQuery(numOfMatches)
        player.getSubPlayers(numOfPlayers)
    return HttpResponse('Got {} SubPlayers, with {} Matches'.format(numOfPlayers, numOfMatches))

def saveAllPlayers(request):
    if request.method == 'GET':
        saveAllPlayersInFolder()
    return HttpResponse('Saved all')

def querySubPlayersAndSavePlayers(request):
    if request.method == 'GET':
        numOfPlayers = int(request.GET.get('numOfPlayers'))
        numOfMatches = int(request.GET.get('numOfMatches'))
        player = tftQuery(numOfMatches)
        player.getSubPlayers(numOfPlayers)

        saveAllPlayersInFolder()

        return HttpResponse('Got {} SubPlayers, with {} Matches and Saved All'.format(numOfPlayers, numOfMatches))











