from tft.models import champion, augment, trait, item, miscellaneous
import ast


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
        raise Exception(f'Failed to get icon for augments in {match_augment}: {e}')


def expandMatchSummonerTraits(data, patch):
    try:
        for match_trait in data:
            traitObject = trait.safe_get_api_name_patch(match_trait['name'], patch)
            match_trait['icon'] = traitObject.icon.split('/')[-1].replace('.dds', '').replace('.tex', '').lower()
            match_trait['display_name'] = traitObject.display_name
        sorted_match_summoner_traits_data = sorted(data, key=lambda d: (d['style'], d['num_units']), reverse=True)
        return sorted_match_summoner_traits_data
    except Exception as e:
        raise Exception(f'Failed to get icon for traits in {match_trait}: {e}')


def expandMatchSummonerUnits(data, patch):
    try:
        for match_unit in data:
            championObject = champion.safe_get_api_name_patch(match_unit['character_id'], patch)
            match_unit['icon'] = championObject.icon.split('/')[-1].replace('.dds', '').replace('.tex', '').lower()
            match_unit['display_name'] = championObject.display_name
            match_unit['items'] = expandMatchSummonerUnitItems(match_unit['itemNames'], patch)
            match_unit['cost'] = championObject.cost
            match_unit.pop('itemNames', None)
        sorted_match_summoner_units_data = sorted(data, key=lambda d: (d['tier'], d['rarity'], len(d['items'])), reverse=True)
        return sorted_match_summoner_units_data
    except Exception as e:
        raise Exception(f'Failed to get icon for units in {match_unit}: {e}')

def expandMatchSummonerUnitItems(data, patch):
    try:
        new_item_list = []
        for match_item in data:
            if '_Item_' in match_item:
                itemObject = item.safe_get_api_name_patch(match_item, patch)
            else:
                itemObject = miscellaneous.safe_get_api_name_patch(match_item, patch)
            new_match_item = {
                'name': match_item,
                'icon': '/'.join(itemObject.icon.split('/')[-2:]).replace('.dds', '').replace('.tex', '').lower(),
                'display_name': itemObject.display_name,
            }
            new_item_list.append(new_match_item)
        return new_item_list
    except Exception as e:
        raise Exception(f'Failed to get icon for items in {match_item}: {e}')
