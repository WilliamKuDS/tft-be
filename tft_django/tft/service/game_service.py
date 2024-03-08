from tft.models import game, player, game_info, patch, trait
from django.forms.models import model_to_dict
from json import dumps


def createGame(data):
    playerID = data['player_id']
    gameID = data['game_id']
    patchID = data['patch_id']
    placement = data['placement']
    level = data['level']
    length = data['length']
    round = data['round']
    augments = data['augment_id']
    headliner = data['headliner_id']
    gameTraits = data['game_trait_id']
    gameUnits = data['game_unit_id']


    gameObject = game.safe_get_player_game_id(player_id=playerID, game_id=gameID)

    if gameObject is not None:
        print("Game {} with player {} already exists in database".format(gameID, playerID))
        gameObject.player_id.add(playerID)
    else:
        player_id = player.safe_get_id(player_id=playerID)
        game_id = game_info.safe_get_game_id(game_id=gameID)
        patch_id = patch.safe_get_patch_id(patch_id=patchID)
        headliner_id = trait.safe_get_id(trait_id=headliner)

        insert_game = game(
            player_id=player_id,
            game_id=game_id,
            patch_id=patch_id,
            placement=placement,
            level=level,
            length=length,
            round=round,
            headliner_id=headliner_id
        )
        insert_game.save()

        for augment in augments:
            insert_game.augment_id.add(augment)

        for traits in gameTraits:
            insert_game.game_trait_id.add(traits)

        for units in gameUnits:
            insert_game.game_unit_id.add(units)

        return insert_game.pk

def readGameByID(data):
    player_game_id = data['player_game_id']

    gameObject = game.safe_get(player_game_id=player_game_id)
    if gameObject is None:
        print("Game {} does not exist in database".format(player_game_id))
    else:
        dictObject = model_to_dict(gameObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData

def readGameByPlayerGame(data):
    playerID = data['player_id']
    gameID = data['game_id']

    gameObject = game.safe_get_player_game_id(player_id=playerID, game_id=gameID)
    if gameObject is None:
        print("Player {} does not exist in database".format(playerID))
    else:
        dictObject = model_to_dict(gameObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def updateGame(data):
    player_game_id = data['player_game_id']
    gameID = data['game_id']
    playerID = data['player_id']
    patchID = data['patch_id']
    placement = data['placement']
    level = data['level']
    length = data['length']
    round = data['round']
    gameAugments = data['augment_id']
    headliner = data['headliner_id']
    gameTraits = data['game_trait_id']
    gameUnits = data['game_unit_id']

    gameObject = game.safe_get(player_game_id=player_game_id)

    if gameObject is None:
        print("Game {} doesn't exist in database".format(gameID))
    else:
        player_id = player.safe_get_id(player_id=playerID)
        game_id = game_info.safe_get_game_id(game_id=gameID)
        patch_id = patch.safe_get_patch_id(patch_id=patchID)
        headliner_id = trait.safe_get_id(trait_id=headliner)

        gameObject.game_id = game_id
        gameObject.player_id = player_id
        gameObject.patch_id = patch_id
        gameObject.placement = placement
        gameObject.level = level
        gameObject.length = length
        gameObject.round = round
        gameObject.headliner_id = headliner_id
        gameObject.save()

        gameObject.augment_id.clear()
        for augments in gameAugments:
            gameObject.augment_id.add(augments)

        gameObject.game_trait_id.clear()
        for traits in gameTraits:
            gameObject.game_trait_id.add(traits)

        gameObject.game_unit_id.clear()
        for units in gameUnits:
            gameObject.game_unit_id.add(units)

        dictObject = model_to_dict(gameObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData

    # else:
    #     gameinfoObject.queue = queue
    #     gameinfoObject.rank = rank
    #     gameinfoObject.save()


def deleteGameByID(data):
    player_game_id = data['player_game_id']

    gameObject = game.safe_get(player_game_id=player_game_id)
    if gameObject is None:
        print("Game {} doesn't exist in database, can't delete".format(player_game_id))
    else:
        gameObject.delete()

def deleteGameByPlayerGame(data):
    playerID = data['player_id']
    gameID = data['game_id']

    gameObject = game.safe_get_player_game_id(player_id=playerID, game_id=gameID)
    if gameObject is None:
        print("Game {} with player {} doesn't exist in database, can't delete".format(playerID, gameID))
    else:
        gameObject.delete()




