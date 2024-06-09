from tft.models import account, summoner, region, summoner_league
from tft.utils.insert_functions import insertAccount, insertSummoner, insertSummonerLeague, insertLeague

from django.forms.models import model_to_dict

from json import dumps
import requests
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime


def createSummoner(data):
    playerName = data['player_name']
    region = data['player_region'].lower()
    lastUpdated = datetime.today()

    playerID = account.safe_get(player_name=playerName, region=region)

    if playerID is not None:
        print("Account {} already exists in database".format(playerName))
    else:
        insert_player = account(
            player_name=playerName,
            region=region,
            last_updated=lastUpdated
        )
        #insert_player.save()
        return insert_player.pk


def readSummoner(puuid, region_id):
    try:
        accountObject = account.safe_get_by_puuid(puuid)
        if accountObject is None:
            raise Exception("Account does not exist in database for {}".format(puuid))

        regionObject = region.safe_get_by_region_id(region_id)
        summonerObject = summoner.safe_get_by_puuid_region(accountObject, regionObject)
        if summonerObject is None:
            raise Exception("Summoner does not exist in database for {}".format(puuid))

        summonerLeagueObject = summoner_league.safe_get_by_summoner_id_and_region(summonerObject, regionObject)
        if summonerLeagueObject is None:
            raise Exception("SummonerLeague does not exist in database for {}".format(puuid))

        summonerDictObject = model_to_dict(summonerObject)
        summonerLeagueDictObject = model_to_dict(summonerLeagueObject)
        dictObject = {**summonerDictObject, **summonerLeagueDictObject}
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData

    except Exception as e:
        raise Exception("Server error in reading player {}: {}".format(puuid, e))

def updateSummoner(data):
    playerID = data['player_id']
    playerName = data['player_name']
    region = data['player_region'].lower()
    lastUpdated = data['last_updated']

    playerObject = account.safe_get_id(player_id=playerID)

    if playerObject is None:
        print("Account {} doesn't exist in database".format(playerName))
    else:
        playerObject.player_name = playerName
        playerObject.region = region
        playerObject.last_updated = lastUpdated
        playerObject.save()

        dictObject = model_to_dict(playerObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def deleteSummoner(data):
    playerID = data['player_id']

    playerObject = account.safe_get_id(player_id=playerID)
    if playerObject is None:
        print("Account {} doesn't exist in database, can't delete".format(playerID))
    else:
        playerObject.delete()


def updateOrCreateAccountByPUUID(puuid, region_id):
    try:
        load_dotenv(find_dotenv())

        # Gets player information from PUUID and saves it to database as player model
        account_response = requests.get(
            "https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}".format(puuid),
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_account_response = account_response.json()
        insertAccount(json_account_response)

        # Gets summoner information from puuid and region and saves it to database as summoner model
        regionObject = region.safe_get_by_region_id(region_id)
        server_code = regionObject.server

        summoner_response = requests.get(
            "https://{}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{}".format(server_code, puuid),
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_summoner_response = summoner_response.json()
        json_summoner_response['region'] = regionObject
        insertSummoner(json_summoner_response)

        summoner_id = json_summoner_response['id']
        summoner_league_response = requests.get(
            "https://{}.api.riotgames.com/tft/league/v1/entries/by-summoner/{}".format(server_code, summoner_id),
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_summoner_league_response = summoner_league_response.json()
        if json_summoner_league_response:
            for summoner_league in json_summoner_league_response:
                league_id = summoner_league['leagueId']
                league_response = requests.get(
                    "https://{}.api.riotgames.com/tft/league/v1/leagues/{}".format(server_code, league_id),
                    headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
                )
                json_league_response = league_response.json()
                json_league_response['region'] = regionObject
                insertLeague(json_league_response)

                summoner_league['region'] = regionObject
                insertSummonerLeague(summoner_league)

        return 200
    except Exception as e:
        print("Failed to update or create player for {}: {}".format(puuid, e))
        return 500

def createUpdateAccount(data):
    try:
        insertAccount(data)
        return 200
    except Exception as e:
        print("Failed to create and/or update player for {}: {}".format(data['puuid'], e))
        return 500