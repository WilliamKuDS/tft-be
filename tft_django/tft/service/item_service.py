from tft.models import item
from django.forms.models import model_to_dict
from json import dumps
from django.core import serializers


def createItem(data):
    name = data['name']
    setID = data['set_id']

    itemObject = item.safe_get_name(name=name, set_id=setID)
    if itemObject is not None:
        print('Item {} already exists'.format(name))
    else:
        item_insert = item(
            name=name,
            set_id=setID
        )
        item_insert.save()
        return item_insert.pk


def readItemID(data):
    itemID = data['item_id']

    itemObject = item.safe_get(item_id=itemID)
    if itemObject is None:
        print('Item {} does not exist'.format(itemID))
    else:
        dictObject = model_to_dict(itemObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def readItemName(data):
    name = data['name']
    setID = data['set_id']

    itemObject = item.safe_get_name(name=name, set_id=setID)
    if itemObject is None:
        print('Item {} does not exist'.format(name))
    else:
        dictObject = model_to_dict(itemObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def readItemAll():
    unitObjects = item.objects.all()
    jsonData = serializers.serialize('json', unitObjects)

    return jsonData


def updateItem(data):
    itemID = data['item_id']
    name = data['name']
    setID = data['set_id']

    itemObject = item.safe_get_id(item_id=itemID)
    if itemObject is None:
        print('Item {} does not exist'.format(itemID))
    else:
        itemObject.name = name
        itemObject.set_id = setID
        itemObject.save()

        dictObject = model_to_dict(itemObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def deleteItemID(data):
    itemID = data['item_id']

    itemObject = item.safe_get_id(item_id=itemID)
    if itemObject is None:
        print('Item {} does not exist'.format(itemID))
    else:
        itemObject.delete()


def deleteItemName(data):
    name = data['name']
    setID = data['set_id']

    itemObject = item.safe_get_name(name=name, set_id=setID)
    if itemObject is None:
        print('Item {} does not exist'.format(name))
    else:
        itemObject.delete()
