from tft.models import item
from django.forms.models import model_to_dict
from json import dumps
from django.core import serializers


def createItem(data):
    pass


def readItem(data):
    pass


def readItemAllByPatch(patch):
    championQuerySet = item.objects.filter(patch_id_id=patch)
    championQuerySet_json = serializers.serialize('json', championQuerySet)
    return championQuerySet_json


def readItemAll():
    unitObjects = item.objects.all()
    jsonData = serializers.serialize('json', unitObjects)

    return jsonData


def updateItem(data):
    pass


def deleteItem(data):
    pass
