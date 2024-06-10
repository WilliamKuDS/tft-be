from tft.utils.insert_functions import insertChampion, insertTrait, insertItem, insertAugment, insertMisc
def read_champion_and_add_to_database(champion, patch_id):
    try:
        champion['patch_id'] = patch_id
        insertChampion(champion)
    except Exception as e:
        raise Exception('Error adding champion to database: {}'.format(e))

def read_trait_and_add_to_database(trait, patch_id):
    try:
        trait['patch_id'] = patch_id
        insertTrait(trait)
    except Exception as e:
        raise Exception('Error adding trait {} to database: {}'.format(trait, e))

def read_item_or_augment_and_add_to_database(data, patch_id):
    try:
        data['patch_id'] = patch_id
        if 'apiName' in data:
            if "_Item_" in data.get('apiName'):
                insertItem(data)
            elif "_Augment_" in data.get('apiName'):
                insertAugment(data)
            else:
                insertMisc(data)
        else:
            if "_Item_" in data.get('icon'):
                insertItem(data)
            elif "_Augment_" in data.get('icon'):
                insertAugment(data)
            else:
                insertMisc(data)
    except Exception as e:
        raise Exception('Error adding data {} to database: {}'.format(data, e))
