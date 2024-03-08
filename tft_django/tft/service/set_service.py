from tft.models import set
from django.forms.models import model_to_dict
from json import dumps


def createSet(data):
    setID = data['set_id']
    setName = data['set_name']
    setType = data['set_type']

    setObject = set.safe_get(set_id=setID)
    if setObject is not None:
        print('Set {} already exists'.format(setID))
    else:
        set_insert = set(
            set_id=setID,
            set_name=setName,
            set_type=setType
        )
        set_insert.save()
        return set_insert.pk


def readSetID(data):
    setID = data['set_id']

    setObject = set.safe_get(set_id=setID)
    if setObject is None:
        print('Set {} does not exist'.format(setID))
    else:
        dictObject = model_to_dict(setObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def readSetName(data):
    setName = data['name']

    setObject = set.safe_get_name(set_name=setName)
    if setObject is None:
        print('Set {} does not exist'.format(setName))
    else:
        dictObject = model_to_dict(setObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def updateSet(data):
    setID = data['set_id']
    setName = data['set_name']
    setType = data['set_type']

    setObject = set.safe_get(set_id=setID)
    if setObject is None:
        print('Set {} does not exist'.format(setID))
    else:
        setObject.set_name = setName
        setObject.set_type = setType
        setObject.save()

        dictObject = model_to_dict(setObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def deleteSet(data):
    setID = data['set_id']

    setObject = set.safe_get(set_id=setID)
    if setObject is None:
        print('Set {} does not exist'.format(setID))
    else:
        setObject.delete()
