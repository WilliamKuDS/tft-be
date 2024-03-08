from tft.models import trait
from django.forms.models import model_to_dict
from json import dumps


def createTrait(data):
    name = data['name']
    setID = data['set_id']

    traitObject = trait.safe_get_name(name=name, set_id=setID)
    if traitObject is not None:
        print('trait {} already exists'.format(name))
    else:
        trait_insert = trait(
            name=name,
            set_id=setID
        )
        trait_insert.save()
        return trait_insert.pk


def readTraitID(data):
    traitID = data['trait_id']

    traitObject = trait.safe_get(trait_id=traitID)
    if traitObject is None:
        print('Trait {} does not exist'.format(traitID))
    else:
        dictObject = model_to_dict(traitObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def readTraitName(data):
    name = data['name']
    setID = data['set_id']

    traitObject = trait.safe_get_name(name=name, set_id=setID)
    if traitObject is None:
        print('Trait {} does not exist'.format(name))
    else:
        dictObject = model_to_dict(traitObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def updateTrait(data):
    traitID = data['trait_id']
    name = data['name']
    setID = data['set_id']

    traitObject = trait.safe_get_id(trait_id=traitID)
    if traitObject is None:
        print('trait {} does not exist'.format(traitID))
    else:
        traitObject.name = name
        traitObject.set_id = setID
        traitObject.save()

        dictObject = model_to_dict(traitObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def deleteTraitID(data):
    traitID = data['trait_id']

    traitObject = trait.safe_get_id(trait_id=traitID)
    if traitObject is None:
        print('Trait {} does not exist'.format(traitID))
    else:
        traitObject.delete()


def deleteTraitName(data):
    name = data['name']
    setID = data['set_id']

    traitObject = trait.safe_get_name(name=name, set_id=setID)
    if traitObject is None:
        print('Trait {} does not exist'.format(name))
    else:
        traitObject.delete()
