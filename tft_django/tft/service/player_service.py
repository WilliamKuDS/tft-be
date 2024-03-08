from tft.models import player
from django.forms.models import model_to_dict
from json import dumps

from datetime import date


def createPlayer(data):
    playerName = data['player_name']
    region = data['player_region'].lower()
    lastUpdated = date.today()

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
    region = data['player_region'].lower()

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
