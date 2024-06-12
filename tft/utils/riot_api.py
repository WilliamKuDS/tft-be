import requests
import os
from dotenv import load_dotenv, find_dotenv
from django.core.cache import cache

load_dotenv(find_dotenv())

class RiotAPIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]})

    def get(self, url, params=None):
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f'Unable to get data from Riot API: {e}')

riot_api_client = RiotAPIClient()

def getAccountFromRiotAPI(puuid):
    cache_key = f"riot_account_{puuid}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
    data = riot_api_client.get(url)
    cache.set(cache_key, data, timeout=60*60)  # Cache for 1 hour
    return data

def getSummonerFromRiotAPI(puuid, server_code):
    cache_key = f"riot_summoner_{server_code}_{puuid}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"https://{server_code}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}"
    data = riot_api_client.get(url)
    cache.set(cache_key, data, timeout=60*60)
    return data

def getLeagueFromRiotAPI(league_id, server_code):
    cache_key = f"riot_league_{server_code}_{league_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"https://{server_code}.api.riotgames.com/tft/league/v1/leagues/{league_id}"
    data = riot_api_client.get(url)
    cache.set(cache_key, data, timeout=60*60)
    return data

def getSummonerLeagueFromRiotAPI(summoner_id, server_code):
    cache_key = f"riot_summoner_league_{server_code}_{summoner_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"https://{server_code}.api.riotgames.com/tft/league/v1/entries/by-summoner/{summoner_id}"
    data = riot_api_client.get(url)
    cache.set(cache_key, data, timeout=60*60)
    return data

def getSummonerMatchListFromRiotAPI(puuid, start, count):
    cache_key = f"riot_summoner_match_list_{puuid}_{start}_{count}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"
    params = {"start": start, "count": count}
    data = riot_api_client.get(url, params=params)
    cache.set(cache_key, data, timeout=60*60)
    return data

def getMatchInfoFromRiotAPI(match_id):
    cache_key = f"riot_match_info_{match_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}"
    data = riot_api_client.get(url)
    cache.set(cache_key, data, timeout=60*60)
    return data
