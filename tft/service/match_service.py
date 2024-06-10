import json

from django.forms import model_to_dict

from tft.models import match_summoner, match, companion
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
    companion_icon_local_location = "/tft/companion/"

    basic_match_data = [
        {
            'match_id': ms_data.match_id_id,
            'puuid': puuid,
            'game_creation': ms_data.match_id.game_creation,
            'placement': ms_data.placement,
            'lobby_rank': None,
            'patch': ms_data.match_id.patch,
            'companion_icon': companion_icon_local_location + companion.safe_get_by_content_id(ms_data.companion['content_ID']).loadout_icon.split('/')[-1].lower()
        }
        for ms_data in match_summoner_data
    ]
    sorted_match_summoner_data = sorted(basic_match_data, key=lambda d: d['game_creation'], reverse=True)

    json_basic_match_data = json.dumps(sorted_match_summoner_data)
    return json_basic_match_data


def getDetailedMatch(puuid, match_id):
    match_info_data = match.safe_get_by_match_id(match_id=match_id)
    serialized_match_info_data = model_to_dict(match_info_data)

    participants_fields = ['match_id', 'puuid', 'placement', 'gold_left', 'last_round', 'level', 'players_eliminated',
                           'time_eliminated', 'total_damage_to_players', 'companion', 'augments', 'traits', 'units']

    participants_data = match_info_data.match_summoner_set.all()
    sorted_participants = participants_data.order_by('placement')
    #modified_participants = [expandMatchData(participant, match_info_data.patch) for participant in sorted_participants]
    serialized_participants_data = serializers.serialize('json', sorted_participants)

    summoner_match_data = participants_data.get(**{'puuid': puuid})
    serialized_summoner_match_data = model_to_dict(summoner_match_data)

    match_data = {
        'match_info': serialized_match_info_data,
        'summoner_match_data': serialized_summoner_match_data,
        'all_summoner_match_data': serialized_participants_data
    }
    json_match_data = json.dumps(match_data)

    return json_match_data
