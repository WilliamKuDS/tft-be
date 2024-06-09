import requests
import os
from dotenv import load_dotenv, find_dotenv

def getAccountFromRiotAPI(puuid):
    try:
        load_dotenv(find_dotenv())
        account_response = requests.get(
            f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}",
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_account_response = account_response.json()
        return json_account_response
    except Exception as e:
        raise Exception(f'Unable to get account from Riot API: {e}')


def getSummonerFromRiotAPI(puuid, server_code):
    try:
        load_dotenv(find_dotenv())
        summoner_response = requests.get(
            f"https://{server_code}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}",
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_summoner_response = summoner_response.json()
        return json_summoner_response
    except Exception as e:
        raise Exception(f'Unable to get summoner from Riot API: {e}')


def getLeagueFromRiotAPI(league_id, server_code):
    try:
        load_dotenv(find_dotenv())
        league_response = requests.get(
            f"https://{server_code}.api.riotgames.com/tft/league/v1/leagues/{league_id}",
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_league_response = league_response.json()
        return json_league_response
    except Exception as e:
        raise Exception(f'Unable to get league from Riot API: {e}')


def getSummonerLeagueFromRiotAPI(summoner_id, server_code):
    try:
        load_dotenv(find_dotenv())
        summoner_league_response = requests.get(
            f"https://{server_code}.api.riotgames.com/tft/league/v1/entries/by-summoner/{summoner_id}",
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_summoner_league_response = summoner_league_response.json()
        return json_summoner_league_response
    except Exception as e:
        raise Exception(f'Unable to get summoner league from Riot API: {e}')

def getSummonerMatchListFromRiotAPI(puuid, start, count):
    summoner_match_list_response = requests.get(
        f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start={start}&count={count}",
        headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
    )
    json_summoner_match_list_response = summoner_match_list_response.json()
    return json_summoner_match_list_response
