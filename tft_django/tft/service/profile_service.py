from tft.models import region, match, account
from tft.utils.insert_functions import insertSummoner, insertSummonerLeague, insertLeague, insertMatch, insertMatchSummoner, insertAccount
from django.db import transaction
import requests
import os
from dotenv import load_dotenv, find_dotenv

def createUpdateProfile(puuid, region_id):
    try:
        load_dotenv(find_dotenv())
        regionObject = region.safe_get_by_region_id(region_id)

        createUpdateSummoner(puuid, regionObject)
        createUpdateSummonerMatches(puuid, regionObject)

        return 200
    except Exception as e:
        print(f"Failed to create or update player profile for {puuid}: {e}")
        return 500

def createUpdateSummoner(puuid, regionObject):
    try:
        server_code = regionObject.server

        summoner_response = requests.get(
            f"https://{server_code}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}",
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_summoner_response = summoner_response.json()
        json_summoner_response['region'] = regionObject
        insertSummoner(json_summoner_response)

        summoner_id = json_summoner_response['id']
        summoner_league_response = requests.get(
            f"https://{server_code}.api.riotgames.com/tft/league/v1/entries/by-summoner/{summoner_id}",
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_summoner_league_response = summoner_league_response.json()
        if json_summoner_league_response:
            for summoner_league in json_summoner_league_response:
                league_id = summoner_league['leagueId']
                league_response = requests.get(
                    f"https://{server_code}.api.riotgames.com/tft/league/v1/leagues/{league_id}",
                    headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
                )
                json_league_response = league_response.json()
                json_league_response['region'] = regionObject
                insertLeague(json_league_response)

                summoner_league['region'] = regionObject
                insertSummonerLeague(summoner_league)
    except Exception as e:
        raise Exception(f"Failed to create or update summoner data: {e}")

def createUpdateSummonerMatches(puuid, regionObject):
    try:
        server_code = regionObject.server
        start = 0
        count = 20

        summoner_match_list_response = requests.get(
            f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start={start}&count={count}",
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_summoner_match_list_response = summoner_match_list_response.json()
        for match_id in json_summoner_match_list_response:
            if not match.objects.filter(match_id=match_id).exists():
                if server_code.upper() in match_id:
                    with transaction.atomic():
                        match_data = {}
                        match_data_response = requests.get(
                            f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}",
                            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
                        )
                        json_match_data_response = match_data_response.json()
                        match_info = json_match_data_response['info']
                        match_metadata = json_match_data_response['metadata']

                        match_data['match_id'] = match_id
                        match_data['game_id'] = match_info['gameId']
                        match_data['region'] = regionObject.region_id
                        match_data['data_version'] = match_metadata['data_version']
                        match_data['game_result'] = match_info['endOfGameResult']
                        match_data['game_creation'] = match_info['gameCreation']
                        match_data['game_datetime'] = match_info['game_datetime']
                        match_data['game_length'] = match_info['game_length']
                        match_data['game_version'] = match_info['game_version']
                        match_data['map_id'] = match_info['mapId']
                        match_data['queue_id'] = match_info['queueId']
                        match_data['game_type'] = match_info['tft_game_type']
                        match_data['set_core_name'] = match_info['tft_set_core_name']
                        match_data['set'] = match_info['tft_set_number']
                        match_data
                        matchObject = insertMatch(match_data)

                        for participant in match_info['participants']:
                            if not account.objects.filter(puuid=participant['puuid']).exists():
                                account_response = requests.get(
                                    f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{participant['puuid']}",
                                    headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
                                )
                                json_account_response = account_response.json()
                                insertAccount(json_account_response)

                                summoner_response = requests.get(
                                    f"https://{server_code}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{participant['puuid']}",
                                    headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
                                )
                                json_summoner_response = summoner_response.json()
                                json_summoner_response['region'] = regionObject
                                insertSummoner(json_summoner_response)

                            participant['match_id'] = matchObject
                            insertMatchSummoner(participant)

            print(f"Finished {match_id}")

    except Exception as e:
        raise Exception(f"Failed to create match data: {e}")


