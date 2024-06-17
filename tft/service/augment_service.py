from tft.models import augment
from django.core import serializers
from django.forms.models import model_to_dict
from json import dumps


def createAugment(data):
    pass


def readAugment(data):
    pass

def readAugmentAllByPatch(patch):
    augmentQuerySet = augment.objects.filter(patch_id_id=patch)
    print(len(augmentQuerySet))
    augmentQuerySet_json = serializers.serialize('json', augmentQuerySet)
    return augmentQuerySet_json

def updateAugment(data):
    pass


def deleteAugment(data):
    pass


