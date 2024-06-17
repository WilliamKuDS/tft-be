from tft.models import patch
from django.utils import timezone
from django.db import models
from django.core import serializers
from django.forms.models import model_to_dict
from json import dumps



def createPatch(data):
    pass


def readPatch(data):
    pass

def readPatchAll():
    patchQuerySet = patch.objects.all()
    patchQuerySetList = list(patchQuerySet.values("patch_id", "set_id_id"))
    return patchQuerySetList


def updatePatch(data):
    pass


def deletePatch(data):
    pass

def getPatchFromDate(current_datetime):
    # First, ensure the current_datetime is timezone-aware
    if timezone.is_naive(current_datetime):
        current_datetime = timezone.make_aware(current_datetime, timezone.get_current_timezone())

    # Find the patch where the current_datetime lands between date_start and date_end
    patchObject = patch.objects.filter(date_start__lte=current_datetime).filter(
        models.Q(date_end__gte=current_datetime) | models.Q(date_end__isnull=True)
    ).order_by('-date_start').first()

    return patchObject.patch_id
