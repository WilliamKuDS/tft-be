from tft.models import item
from django.forms.models import model_to_dict
from json import dumps
from django.core import serializers


def createItem(data):
    pass


def readItem(data):
    pass




def readItemAll():
    unitObjects = item.objects.all()
    jsonData = serializers.serialize('json', unitObjects)

    return jsonData


def updateItem(data):
    pass




def deleteItem(data):
    pass
