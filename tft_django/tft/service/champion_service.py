from tft.models import champion
from json import dumps
from django.forms.models import model_to_dict
from django.core import serializers


def createChampion(data):
    pass



def readChampion(data):
    pass

def readChampionAll():
    unitObjects = champion.objects.all()
    jsonData = serializers.serialize('json', unitObjects)

    return jsonData


def updateChampion(data):
    pass


def deleteChampion(data):
    pass
