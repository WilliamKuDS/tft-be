import traceback

from tft.models import region, match, account
from tft.service.patch_service import getPatchFromDate
from tft.utils.convert_unix_to_datetime import convert_unix_to_datetime
from tft.utils.insert_functions import insertSummoner, insertSummonerLeague, insertLeague, insertMatch, \
    insertMatchSummoner, insertAccount
from django.db import transaction
import requests
import os
from dotenv import load_dotenv, find_dotenv

from tft.utils.riot_api import getAccountFromRiotAPI, getSummonerFromRiotAPI, getSummonerLeagueFromRiotAPI, \
    getLeagueFromRiotAPI, getSummonerMatchListFromRiotAPI


def createUpdateProfile(puuid, region_id):
    try:
        load_dotenv(find_dotenv())
        regionObject = region.safe_get_by_region_id(region_id)

        createUpdateSummoner(puuid, regionObject)
        createUpdateSummonerMatches(puuid, regionObject)

        return 200
    except Exception as e:
        print(f"Failed to create or update player profile for {puuid}: {e}")
        traceback.print_exc()
        return 500


def createUpdateSummoner(puuid, regionObject):
    try:
        with transaction.atomic():
            server_code = regionObject.server
            json_account_response = getAccountFromRiotAPI(puuid)
            insertAccount(json_account_response)

            json_summoner_response = getSummonerFromRiotAPI(puuid, server_code)
            json_summoner_response['region'] = regionObject
            insertSummoner(json_summoner_response)

            summoner_id = json_summoner_response['id']
            updateLeagueAndSummonerLeague(summoner_id, regionObject)

    except Exception as e:
        raise Exception(f"Failed to create or update summoner data: {e}")

def updateLeagueAndSummonerLeague(summoner_id, regionObject):
    server_code = regionObject.server
    json_summoner_league_response = getSummonerLeagueFromRiotAPI(summoner_id, server_code)
    if json_summoner_league_response:
        for summoner_league in json_summoner_league_response:
            # Ignore RANKED_TFT_TURBO leagues
            if summoner_league['queueType'] == 'RANKED_TFT':
                league_id = summoner_league['leagueId']

                json_league_response = getLeagueFromRiotAPI(league_id, server_code)
                json_league_response['region'] = regionObject
                insertLeague(json_league_response)

                summoner_league['region'] = regionObject
                insertSummonerLeague(summoner_league)


def createUpdateSummonerMatches(puuid, regionObject):
    try:
        server_code = regionObject.server
        start = 0
        count = 20

        json_summoner_match_list_response = getSummonerMatchListFromRiotAPI(puuid, start, count)
        for match_id in json_summoner_match_list_response:
            try:
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
                            match_datetime = convert_unix_to_datetime(match_data['game_creation'])
                            match_data['patch'] = getPatchFromDate(match_datetime)
                            matchObject = insertMatch(match_data)

                            for participant in match_info['participants']:
                                if not account.objects.filter(puuid=participant['puuid']).exists():
                                    createUpdateSummoner(participant['puuid'], regionObject)

                                #participant['region'] = regionObject
                                participant['match_id'] = matchObject
                                insertMatchSummoner(participant)

                print(f"Finished {match_id}")
            except Exception as e:
                print(f'Failed to get {match_id}: {e}')
                continue

    except Exception as e:
        raise Exception(f"Failed to create match data: {e}")



