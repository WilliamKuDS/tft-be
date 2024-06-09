from tft.models import match_summoner
from django.core import serializers
def createMatch(data):
    pass

def readMatch(puuid, region):
    match_data = match_summoner.objects.filter(puuid=puuid, match_id__region=region)
    jsonData = serializers.serialize('json', match_data)
    return jsonData


def updateMatch(data):
    pass

def deleteMatch(data):
    pass