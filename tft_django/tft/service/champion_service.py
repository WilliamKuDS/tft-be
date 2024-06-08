from tft.models import champion
from json import dumps
from django.forms.models import model_to_dict
from django.core import serializers


def createUnit(data):
    name = data['name']
    trait = data['trait']
    setID = data['set_id']

    unitObject = champion.safe_get_name(name=name, set_id=setID)
    if unitObject is not None:
        print('Unit {} already exists'.format(name))
    else:
        unit_insert = champion(
            name=name,
            trait=trait,
            set_id=setID
        )
        unit_insert.save()
        return unit_insert.pk



def readUnitID(data):
    unitID = data['unit_id']

    unitObject = champion.safe_get(unit_id=unitID)
    if unitObject is None:
        print('Unit {} does not exist'.format(unitID))
    else:
        dictObject = model_to_dict(unitObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def readUnitName(data):
    name = data['name']
    setID = data['set_id']

    unitObject = champion.safe_get_name(name=name, set_id=setID)
    if unitObject is None:
        print('Unit {} does not exist'.format(name))
    else:
        dictObject = model_to_dict(unitObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData

def readUnitAll():
    unitObjects = champion.objects.all()
    jsonData = serializers.serialize('json', unitObjects)

    return jsonData


def updateUnit(data):
    unitID = data['unit_id']
    name = data['name']
    trait = data['trait']
    setID = data['set_id']

    unitObject = champion.safe_get_id(unit_id=unitID)
    if unitObject is None:
        print('Unit {} does not exist'.format(unitID))
    else:
        unitObject.name = name
        unitObject.trait = trait
        unitObject.set_id = setID
        unitObject.save()

        dictObject = model_to_dict(unitObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def deleteUnitID(data):
    unitID = data['unit_id']

    unitObject = champion.safe_get_id(unit_id=unitID)
    if unitObject is None:
        print('Unit {} does not exist'.format(unitID))
    else:
        unitObject.delete()


def deleteUnitName(data):
    name = data['name']
    setID = data['set_id']

    unitObject = champion.safe_get_name(name=name, set_id=setID)
    if unitObject is None:
        print('Unit {} does not exist'.format(name))
    else:
        unitObject.delete()
