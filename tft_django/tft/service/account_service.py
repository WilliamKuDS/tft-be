from tft.models import account
from tft.utils.insert_functions import insertAccount
from django.forms.models import model_to_dict
from json import dumps
import requests
import os
from dotenv import load_dotenv, find_dotenv


def createAccount(puuid):
    load_dotenv(find_dotenv())
    try:
        account_response = requests.get(
            "https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}".format(puuid),
            headers={"X-Riot-Token": os.environ["TFT_RIOT_API_KEY"]},
        )
        json_account_response = account_response.json()
        insertAccount(json_account_response)
    except Exception as e:
        raise Exception("Failed to create account: {}".format(e))

def readAccount(data):
    pass



def updateAccount(data):
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


def deleteAccount(data):
    playerID = data['player_id']

    playerObject = account.safe_get_id(player_id=playerID)
    if playerObject is None:
        print("Account {} doesn't exist in database, can't delete".format(playerID))
    else:
        playerObject.delete()

def createUpdateAccount(data):
    try:
        insertAccount(data)
        return 200
    except Exception as e:
        print("Failed to create and/or update player for {}: {}".format(data['puuid'], e))
        return 500
