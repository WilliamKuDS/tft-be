from tft.models import player
from django.forms.models import model_to_dict
from json import dumps
import requests
import os
from dotenv import load_dotenv, find_dotenv

from datetime import datetime
from django.utils import timezone


def createPlayer(data):
    playerName = data['player_name']
    region = data['player_region'].lower()
    lastUpdated = datetime.today()

    playerID = player.safe_get(player_name=playerName, region=region)

    if playerID is not None:
        print("Player {} already exists in database".format(playerName))
    else:
        insert_player = player(
            player_name=playerName,
            region=region,
            last_updated=lastUpdated
        )
        insert_player.save()
        return insert_player.pk

def updateOrCreatePlayerByPUUID(puuid, region):
    try:
        load_dotenv(find_dotenv())

        account_response = requests.get(
            "https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}".format(puuid),
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_account_response = account_response.json()

        summoner_response = requests.get(
            "https://{}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{}".format(region, puuid),
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_summoner_response = summoner_response.json()
        summoner_id = json_summoner_response['id']

        league_response = requests.get(
            "https://{}.api.riotgames.com/tft/league/v1/entries/by-summoner/{}".format(region, summoner_id),
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_league_response = league_response.json()[0]

        lookup_params = {'puuid': puuid,}
        player_dict = {
            'last_updated': timezone.now(),
            'account_id': json_summoner_response['accountId'],
            'summoner_id': summoner_id,
            'game_name': json_account_response['gameName'],
            'tag_line': json_account_response['tagLine'],
            'region': region,
            'icon': json_summoner_response['profileIconId'],
            'level': json_summoner_response['summonerLevel'],
            'league_id': json_league_response['leagueId'],
            'tier': json_league_response['tier'],
            'rank': json_league_response['rank'],
            'league_points': json_league_response['leaguePoints'],
            'wins': json_league_response['wins'],
            'losses': json_league_response['losses'],
            'veteran': json_league_response['veteran'],
            'inactive': json_league_response['inactive'],
            'fresh_blood': json_league_response['freshBlood'],
            'hot_streak': json_league_response['hotStreak']
        }
        player_obj, created = player.objects.update_or_create(
            defaults=player_dict,
            **lookup_params
        )
        return 200
    except Exception as e:
        print("Failed to update or create player for {}: {}".format(puuid, e))
        return 500

def readPlayerID(data):
    playerID = data['player_id']

    playerObject = player.safe_get_id(player_id=playerID)

    if playerObject is None:
        print("Player {} does not exist in database".format(playerID))
    else:
        dictObject = model_to_dict(playerObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def readPlayerValues(data):
    playerName = data['player_name']
    region = data['region'].lower()

    playerObject = player.safe_get(player_name=playerName, region=region)

    if playerObject is None:
        print("Player {} does not exist in database".format(playerName))
    else:
        dictObject = model_to_dict(playerObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def updatePlayer(data):
    playerID = data['player_id']
    playerName = data['player_name']
    region = data['player_region'].lower()
    lastUpdated = data['last_updated']

    playerObject = player.safe_get_id(player_id=playerID)

    if playerObject is None:
        print("Player {} doesn't exist in database".format(playerName))
    else:
        playerObject.player_name = playerName
        playerObject.region = region
        playerObject.last_updated = lastUpdated
        playerObject.save()

        dictObject = model_to_dict(playerObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def deletePlayerID(data):
    playerID = data['player_id']

    playerObject = player.safe_get_id(player_id=playerID)
    if playerObject is None:
        print("Player {} doesn't exist in database, can't delete".format(playerID))
    else:
        playerObject.delete()


def deletePlayerValues(data):
    playerName = data['player_name']
    region = data['player_region'].lower()

    playerObject = player.safe_get(player_name=playerName, region=region)
    if playerObject is None:
        print("Player {} doesn't exist in database, can't delete".format(playerName))
    else:
        playerObject.delete()
