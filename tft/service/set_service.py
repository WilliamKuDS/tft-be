from tft.models import set as set_model
from django.core import serializers
from django.forms.models import model_to_dict
from json import dumps


def createSet(data):
    pass


def readSet(data):
    pass


def readSetAll():
    setQuerySet = set_model.objects.all()
    setQuerySet_json = serializers.serialize('json', setQuerySet)
    return setQuerySet_json


def updateSet(data):
    pass


def deleteSet(data):
    pass
