from tft.models import augment
from django.forms.models import model_to_dict
from json import dumps


def createAugment(data):
    name = data['name']
    tier = data['tier']
    setID = data['set_id']

    augmentObject = augment.safe_get_name(name=name, set_id=setID)
    if augmentObject is not None:
        print('Augment {} already exists'.format(name))
    else:
        augment_insert = augment(
            name=name,
            tier=tier,
            set_id=setID
        )
        augment_insert.save()
        return augment_insert.pk


def readAugmentID(data):
    augmentID = data['augment_id']

    augmentObject = augment.safe_get(augment_id=augmentID)
    if augmentObject is None:
        print('Augment {} does not exist'.format(augmentID))
    else:
        dictObject = model_to_dict(augmentObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def readAugmentName(data):
    name = data['name']
    setID = data['set_id']

    augmentObject = augment.safe_get_name(name=name, set_id=setID)
    if augmentObject is None:
        print('Augment {} does not exist'.format(name))
    else:
        dictObject = model_to_dict(augmentObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def updateAugment(data):
    augmentID = data['Augment_id']
    name = data['name']
    tier = data['tier']
    setID = data['set_id']

    augmentObject = augment.safe_get_id(augment_id=augmentID)
    if augmentObject is None:
        print('Augment {} does not exist'.format(augmentID))
    else:
        augmentObject.name = name
        augmentObject.tier = tier
        augmentObject.set_id = setID
        augmentObject.save()

        dictObject = model_to_dict(augmentObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def deleteAugmentID(data):
    augmentID = data['augment_id']

    augmentObject = augment.safe_get_id(augment_id=augmentID)
    if augmentObject is None:
        print('Augment {} does not exist'.format(augmentID))
    else:
        augmentObject.delete()


def deleteAugmentName(data):
    name = data['name']
    setID = data['set_id']

    augmentObject = augment.safe_get_name(name=name, set_id=setID)
    if augmentObject is None:
        print('Augment {} does not exist'.format(name))
    else:
        augmentObject.delete()
