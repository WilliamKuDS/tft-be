import json

from tft.models import match_summoner, match
from django.core import serializers
def createMatch(data):
    pass

def readMatch(puuid, region):
    match_summoner_data = match_summoner.objects.filter(puuid=puuid, match_id__region=region)
    match_ids = match_summoner_data.values_list('match_id', flat=True)
    match_data = match.objects.filter(match_id__in=match_ids)

    matchSummonerJsonData = serializers.serialize('json', match_summoner_data)
    matchJsonData = serializers.serialize('json', match_data)


    combinedJSONData = {
        'match_info': matchJsonData,
        'match_summoner_data': matchSummonerJsonData
    }
    combined_json = json.dumps(combinedJSONData)

    return combined_json


def updateMatch(data):
    pass

def deleteMatch(data):
    pass

def getBasicMatch(puuid, region):
    match_summoner_data = match_summoner.objects.filter(puuid=puuid, match_id__region=region)

    basic_match_data = [
        {
            'match_id': ms_data.match_id_id,
            'placement': ms_data.placement,
            'lobby_rank': None,  # Assuming you have this field in MatchSummoner
            'patch': ms_data.match_id.patch
        }
        for ms_data in match_summoner_data
    ]

    json_basic_match_data = json.dumps(basic_match_data)
    return json_basic_match_data


def getDetailedMatch(match_id):
    match_info_data = match.safe_get_by_match_id(match_id=match_id)
    participants_data = match_info_data.match_summoner_set.all()
    serialized_match_info_data = serializers.serialize('json', [match_info_data])
    serialized_participants_data = serializers.serialize('json', participants_data)

    match_data = {
        'match_info': serialized_match_info_data,
        'match_summoner_data': serialized_participants_data
    }
    json_match_data = json.dumps(match_data)

    return json_match_data
