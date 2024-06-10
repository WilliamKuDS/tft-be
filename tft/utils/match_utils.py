from tft.models import champion, augment, trait


def expandMatchSummonerAugments(data, patch):
    try:
        new_augment_data = []
        for match_augment in data:
            augmentObject = augment.safe_get_api_name_patch(match_augment, patch)
            new_match_augment = {
                'name': match_augment,
                'icon': augmentObject.icon.split('/')[-1].replace('.dds', '').replace('.tex', '').lower(),
                'display_name': augmentObject.display_name,
            }
            new_augment_data.append(new_match_augment)
        return new_augment_data
    except Exception as e:
        raise Exception(f'Failed to get icon for augments in {data}: {e}')


def expandMatchSummonerTraits(data, patch):
    try:
        for match_trait in data:
            traitObject = trait.safe_get_api_name_patch(match_trait['name'], patch)
            match_trait['icon'] = traitObject.icon.split('/')[-1].replace('.dds', '').replace('.tex', '').lower()
            match_trait['display_name'] = traitObject.display_name
        return data
    except Exception as e:
        raise Exception(f'Failed to get icon for traits in {data}: {e}')


def expandMatchSummonerUnits(data, patch):
    try:
        for match_unit in data:
            championObject = champion.safe_get_api_name_patch(match_unit['character_id'], patch)
            match_unit['icon'] = championObject.icon.split('/')[-1].replace('.dds', '').replace('.tex', '').lower()
            match_unit['display_name'] = championObject.display_name
        return data
    except Exception as e:
        raise Exception(f'Failed to get icon for units in {data}: {e}')