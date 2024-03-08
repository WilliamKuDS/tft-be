from tft.models import game_trait, trait
from django.forms.models import model_to_dict
from json import dumps


def createGameTrait(data):
    traitID = data['trait_id']
    count = data['count']

    gameTraitObject = game_trait.safe_get_trait(trait_id=traitID, count=count)

    if gameTraitObject is not None:
        print("Trait {} with count {} already exists in database".format(traitID, count))
        return gameTraitObject.pk
    else:
        traitObject = trait.safe_get_id(trait_id=traitID)
        insert_game_trait = game_trait(
            trait_id=traitObject,
            count=count
        )
        insert_game_trait.save()
        return insert_game_trait.pk


def readGameTrait(data):
    gameTraitID = data['game_trait_id']

    gameTraitObject = game_trait.safe_get(game_trait_id=gameTraitID)
    if gameTraitObject is None:
        print("Game Trait {} does not exist in database".format(gameTraitID))
    else:
        dictObject = model_to_dict(gameTraitObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def updateGameTrait(data):
    gameTraitID = data['game_trait_id']
    traitID = data['trait_id']
    count = data['count']

    gameTraitObject = game_trait.safe_get(game_trait_id=gameTraitID)

    if gameTraitObject is None:
        print("Game Trait {} doesn't exist in database".format(gameTraitID))
    else:
        traitObject = trait.safe_get_id(trait_id=traitID)
        gameTraitObject.trait_id = traitObject
        gameTraitObject.count = count
        gameTraitObject.save()

        dictObject = model_to_dict(gameTraitObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def deleteGameTrait(data):
    gameTraitID = data['game_trait_id']

    gameTraitObject = game_trait.safe_get(game_trait_id=gameTraitID)
    if gameTraitObject is None:
        print("Game Trait {} doesn't exist in database, can't delete".format(gameTraitID))
    else:
        gameTraitObject.delete()
