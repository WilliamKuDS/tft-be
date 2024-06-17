from tft.models import trait
from django.forms.models import model_to_dict
from json import dumps
from django.core import serializers


def createTrait(data):
    pass


def readTrait(data):
    pass

def readTraitAllByPatch(patch):
    championQuerySet = trait.objects.filter(patch_id_id=patch)
    championQuerySet_json = serializers.serialize('json', championQuerySet)
    return championQuerySet_json


def updateTrait(data):
    pass


def deleteTrait(data):
    pass

