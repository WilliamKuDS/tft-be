import json

from django.db import IntegrityError

from tft.models import game_info, player, game
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from json import dumps
from json import loads


def createGameInfo(data):
    gameID = data['game_id']
    queue = data['queue']
    lobby_rank = data['lobby_rank']
    playerID = data['player_id']

    gameinfoObject = game_info.safe_get_game_id(game_id=gameID)
    gameinfoObjectPlayer = game_info.safe_get_player_id(player_id=playerID)
    playerObject = player.safe_get_id(player_id=playerID)

    if gameinfoObject is not None:
        if playerObject is None:
            print("Game {} already exists in database, however player {} does not exist".format(gameID, playerID))
            return gameinfoObject.pk
        else:
            if gameinfoObjectPlayer is None:
                print("Game {} already exists in database, adding player {} to it".format(gameID, playerID))
                gameinfoObject.player_id.add(playerID)
                return gameinfoObject.pk
            else:
                print("Game {} with player {} already exists in database".format(gameID, playerID))
                return gameinfoObject.pk
    else:
        insert_game_info = game_info(
            game_id=gameID,
            queue=queue,
            lobby_rank=lobby_rank,
        )
        insert_game_info.save()
        insert_game_info.player_id.add(playerID)
        return insert_game_info.pk


def readGameInfoGameID(data):
    gameID = data['game_id']

    gameinfoObject = game_info.safe_get_game_id(game_id=gameID)
    if gameinfoObject is None:
        print("Game {} does not exist in database".format(gameID))
    else:
        dictObject = model_to_dict(gameinfoObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def readGameInfoPlayerID(data):
    playerID = data['player_id']

    gameinfoObject = game_info.safe_get_player_id(player_id=playerID)
    if gameinfoObject is None:
        print("Player {} does not exist in database".format(playerID))
    else:
        serialized_data = serialize("json", gameinfoObject)
        return serialized_data

def readGameInfoPlayerName(data):
    playerName = data['player_name']
    playerRegion = data['region']
    playerID = player.safe_get(player_name=playerName, region=playerRegion).pk
    gameinfoObject = game_info.safe_get_player_id(player_id=playerID)
    if gameinfoObject is None:
        print("Player {} does not exist in database".format(playerID))
    else:
        modified_gameinfoObject = gameinfoObject.values()
        for item in modified_gameinfoObject:
            gameData = game.safe_get_player_game_id(player_id=playerID, game_id=item['game_id'])
            item['icon'] = gameData.icon
            item['placement'] = gameData.placement
        print(type(modified_gameinfoObject))
        #serialized_data = serialize("json", modified_gameinfoObject)
        #print(serialized_data)
        gameinfoObjectWithPlayer = {
            'gameinfo': list(modified_gameinfoObject),
            'playerID': playerID,
        }
        jsonData = json.dumps(gameinfoObjectWithPlayer, indent=4, sort_keys=True, default=str)
        print(jsonData)
        return jsonData



def updateGameInfo(data):
    gameID = data['game_id']
    queue = data['queue']
    lobby_rank = data['lobby_rank']
    playerID = data['player_id']

    gameinfoObject = game_info.safe_get_game_id(game_id=gameID)

    if gameinfoObject is None:
        print("Game {} doesn't exist in database".format(gameID))
    else:
        gameinfoObject.queue = queue
        gameinfoObject.lobby_rank = lobby_rank
        gameinfoObject.save()

        gameinfoObject.player_id.clear()
        for player_id in playerID:
            try:
                gameinfoObject.player_id.add(player_id)
            except IntegrityError:
                print("Player {} doesn't exists".format(player_id))

        dictObject = model_to_dict(gameinfoObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData

    # else:
    #     gameinfoObject.queue = queue
    #     gameinfoObject.rank = rank
    #     gameinfoObject.save()


def deleteGameInfoGameID(data):
    gameID = data['game_id']

    gameinfoObject = game_info.safe_get_game_id(game_id=gameID)
    if gameinfoObject is None:
        print("Game {} doesn't exist in database, can't delete".format(gameID))
    else:
        gameinfoObject.delete()
