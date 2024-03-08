from tft.models import patch
from django.forms.models import model_to_dict
from json import dumps



def createPatch(data):
    patchID = data['patch_id']
    setID = data['set_id']
    revivalSetID = data['revival_set_id']
    dateStart = data['date_start']
    dateEnd = data['date_end']

    patchObject = patch.safe_get_patch_id(patch_id=patchID)
    if patchObject is not None:
        print('Patch {} already exists'.format(patchID))
    else:
        patch_insert = patch(
            patch_id=patchID,
            set_id=setID,
            revival_set_id=revivalSetID,
            date_start=dateStart,
            date_end=dateEnd
        )
        patch_insert.save()
        return patch_insert.pk


def readPatchID(data):
    patchID = data['patch_id']

    patchObject = patch.safe_get(patch_id=patchID)
    if patchObject is None:
        print('patch {} does not exist'.format(patchID))
    else:
        dictObject = model_to_dict(patchObject)
        jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

        return jsonData


def readPatchSetID(data):
    setID = data['set_id']
    set_type = data['set_type']

    if set_type == 'Main':
        patchObject = patch.safe_get_set_id(set_id=setID)
        if patchObject is None:
            print('patch {} does not exist'.format(setID))
        else:
            dictObject = model_to_dict(patchObject)
            jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

            return jsonData
    else:
        patchObject = patch.safe_get_set_revival_id(revival_set_id=setID)
        if patchObject is None:
            print('patch {} does not exist'.format(setID))
        else:
            dictObject = model_to_dict(patchObject)
            jsonData = dumps(dictObject, indent=4, sort_keys=True, default=str)

            return jsonData


def updatePatch(data):
    patchID = data['patch_id']
    setID = data['set_id']
    revivalSetID = data['revival_set_id']
    dateStart = data['date_start']
    dateEnd = data['date_end']

    patchObject = patch.safe_get(patch_id=patchID)
    if patchObject is None:
        print('patch {} does not exist'.format(patchID))
    else:
        patchObject.set_id = setID
        patchObject.revival_set_id = revivalSetID
        patchObject.date_start = dateStart
        patchObject.date_end = dateEnd
        patchObject.save()


def deletePatch(data):
    patchID = data['patch_id']

    patchObject = patch.safe_get(patch_id=patchID)
    if patchObject is None:
        print('patch {} does not exist'.format(patchID))
    else:
        patchObject.delete()
