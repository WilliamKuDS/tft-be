from tft.models import game_unit, trait, unit, patch, item
from django.forms.models import model_to_dict
from json import dumps


def createGameUnit(data):
    unitID = data['unit_id']
    patchID = data['patch_id']
    star = data['star']
    itemList = data['item']

    gameUnitObject = game_unit.safe_get_unit(unit_id=unitID, patch_id=patchID, star=star, items=itemList)

    if gameUnitObject is not None:
        print("Unit {} with patch {}, star {}, and items {} already exists in database".format(unitID, patchID, star,
                                                                                               itemList))
        return gameUnitObject.pk
    else:
        unitObject = unit.safe_get_id(unit_id=unitID)
        patchObject = patch.safe_get_patch_id(patch_id=patchID)
        insert_game_unit = game_unit(
            unit_id=unitObject,
            patch_id=patchObject,
            star=star
        )
        insert_game_unit.save()

        for items in itemList:
            insert_game_unit.item.add(items)

        return insert_game_unit.pk


def readGameUnit(data):
    gameUnitID = data['game_unit_id']

    gameUnitObject = game_unit.safe_get(game_unit_id=gameUnitID)

    if gameUnitObject is None:
        print("Game Unit {} does not exist in database".format(gameUnitID))
    else:
        dictObject = model_to_dict(gameUnitObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def updateGameUnit(data):
    gameUnitID = data['game_unit_id']
    unitID = data['unit_id']
    patchID = data['patch_id']
    star = data['star']
    itemList = data['item']

    gameUnitObject = game_unit.safe_get(game_unit_id=gameUnitID)

    if gameUnitObject is None:
        print("Game Trait {} doesn't exist in database".format(gameUnitID))
    else:
        unitObject = unit.safe_get_id(unit_id=unitID)
        patchObject = patch.safe_get_patch_id(patch_id=patchID)
        gameUnitObject.unit_id = unitObject
        gameUnitObject.patch_id = patchObject
        gameUnitObject.star = star
        gameUnitObject.save()

        gameUnitObject.trait.clear()
        for items in itemList:
            gameUnitObject.item.add(items)

        dictObject = model_to_dict(gameUnitObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def deleteGameUnit(data):
    gameUnitID = data['game_unit_id']

    gameUnitObject = game_unit.safe_get(game_unit_id=gameUnitID)

    if gameUnitObject is None:
        print("Game Trait {} doesn't exist in database, can't delete".format(gameUnitID))
    else:
        gameUnitObject.delete()
