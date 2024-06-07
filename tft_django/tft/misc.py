from datetime import date
import re

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils import timezone

from tft.models import account, region, summoner, league, summoner_league
from tft.models import set, patch, trait, trait_effect, unit, item, augment


def insertAccount(data):
    try:
        account_lookup_params = {'puuid': data['puuid']}
        account_dict = {
            'game_name': data['gameName'],
            'tag_line': data['tagLine'],
        }

        account_obj, account_created = account.objects.update_or_create(
            defaults=account_dict,
            **account_lookup_params
        )

        return account_obj, account_created

    except Exception as e:
        raise Exception("Error inserting account {}. Error: {}".format(data['puuid'], e))


def insertRegion(data):
    try:
        region_lookup_params = {'region_id': data['region_id']}
        region_dict = {
            'label': data['label'],
            'server': data['server'],
            'description': data['description'],
        }

        region_obj, region_created = region.objects.update_or_create(
            defaults=region_dict,
            **region_lookup_params
        )

        return region_obj, region_created

    except Exception as e:
        raise Exception("Error inserting region {}. Error: {}".format(data['region_id'], e))


def insertSummoner(data):
    try:
        accountObject = account.safe_get_by_puuid(data['puuid'])
        summoner_lookup_params = {'summoner_id': data['id'], 'region': data['region']}
        summoner_dict = {
            'puuid': accountObject,
            'account_id': data['accountId'],
            'icon': data['profileIconId'],
            'level': data['summonerLevel'],
            'last_updated': timezone.now(),
        }
        summoner_obj, summoner_created = summoner.objects.update_or_create(
            defaults=summoner_dict,
            **summoner_lookup_params
        )

        return summoner_obj, summoner_created

    except Exception as e:
        raise Exception("Error inserting summoner {}. Error: {}".format(data['id'], e))


def insertLeague(data):
    try:
        league_lookup_params = {'league_id': data['leagueId'], 'region': data['region']}
        league_dict = {
            'tier': data['tier'],
            'name': data['name'],
            'queue': data['queue']
        }
        league_obj, league_created = league.objects.update_or_create(
            defaults=league_dict,
            **league_lookup_params
        )

        return league_obj, league_created

    except Exception as e:
        raise Exception("Error inserting league {}. Error: {}".format(data['leagueId'], e))


def insertSummonerLeague(data):
    try:
        accountObject = account.safe_get_by_puuid(data['puuid'])
        summonerObject = summoner.safe_get_by_summoner_id(data['summonerId'])
        leagueObject = league.safe_get_by_league_id(data['leagueId'])
        summoner_league_lookup_params = {'summoner_id': summonerObject.id, 'region': data['region'],
                                         'queue': data['queueType']}
        summoner_league_dict = {
            'puuid': accountObject,
            'league_id': leagueObject.id,
            'tier': data['tier'],
            'rank': data['rank'],
            'league_points': data['leaguePoints'],
            'wins': data['wins'],
            'losses': data['losses'],
            'veteran': data['veteran'],
            'inactive': data['inactive'],
            'fresh_blood': data['freshBlood'],
            'hot_streak': data['hotStreak']
        }
        summoner_league_obj, summoner_league_created = summoner_league.objects.update_or_create(
            defaults=summoner_league_dict,
            **summoner_league_lookup_params
        )

        return summoner_league_obj, summoner_league_created

    except Exception as e:
        raise Exception("Error inserting SummonerLeague {}. Error: {}".format(data['summonerId'], e))


def insertSet(data):
    try:
        setID = data['set_id']
        setObject = set.safe_get(set_id=setID)
        if setObject is not None:
            print("Set {} already exists in database".format(setID))
        else:
            insert_set = set(
                set_id=setID,
                set_name=data['set_name']
            )
            insert_set.save()

    except ValueError as e:
        raise Exception("Set {} input incorrect. Error: {}".format(setID, e))


def insertPatch(data):
    try:
        patchID = data['patch_id']
        patchObject = patch.safe_get_patch_id(patch_id=patchID)
        if patchObject is not None:
            print("Patch {} already exists in database".format(data['patch_id']))
        else:
            setID = set.objects.get(set_id=float(data['set_id']))
            insert_patch = patch(
                patch_id=patchID,
                set_id=setID,
                date_start=data['date_start'],
                date_end=data['date_end'],
                highlights=data['highlights'],
                patch_url=data['patch_url']
            )
            insert_patch.save()

    except ValueError as e:
        raise Exception("Patch {} input incorrect. Error: {}".format(data['patch_id'], e))


def insertTrait(data):
    try:
        patch_id = patch.safe_get_patch_id(data['patch_id'])
        if 'apiName' in data:
            api_name = data['apiName']
        else:
            api_name = 'TFT' + str(int(patch_id.set_id.set_id)) + '_' + data['name']

        traitObject = trait.safe_get_api_name_patch(api_name=api_name, patch_id=patch_id)
        if traitObject is not None:
            print("Trait {} already exists in database, skipping".format(api_name))
            return traitObject
        else:
            insert_trait = trait(
                api_name=api_name,
                patch_id=patch_id,
                display_name=data['name'],
                description=data['desc'],
                icon=data['icon'],
            )
            insert_trait.save()
            return insert_trait

    except Exception as e:
        raise Exception("Trait {} input incorrect. Error: {}".format(data, e))

def insertTraitEffects(data):
    try:
        trait_id = data['trait']
        min_units = data['minUnits']
        max_units = data['maxUnits']

        traitEffectsObject = trait_effect.safe_get_trait_id_min_max(trait_id, min_units, max_units)
        if traitEffectsObject is not None:
            print("TraitEffect for {} [{}:{}] already exists in database, skipping".format(trait_id, min_units, max_units))
        else:
            if 'style' in data:
                style = data['style']
            else:
                style = None

            insert_trait_effect = trait_effect(
                trait_id=trait_id,
                style=style,
                min_units=min_units,
                max_units=max_units,
                variables=data['variables'],
            )
            insert_trait_effect.save()

    except Exception as e:
        raise Exception("TraitEffect for {} [{}:{}] input incorrect. Error: {}".format(trait_id, min_units, max_units, e))


def insertAugment(data):
    try:
        name = data['name']
        tier = data['tier']
        icon = data['icon']
        display_name = data['display_name']
        description = data['description']
        set_id = float(data['set_id'])

        augmentObject = augment.safe_get_name(name=name, set_id=set_id)

        if augmentObject is not None:
            print("Augment {} already exists in database, skipping.".format(name))
        else:
            set_id = set.objects.get(set_id=set_id)
            insert_patch = augment(
                name=name,
                display_name=display_name,
                tier=tier,
                icon=icon,
                description=description,
                set_id=set_id
            )
            insert_patch.save()
    except Exception as e:
        print("Augment {} input incorrect. Error: {}".format(name, e))

def insertItem(data):
    try:
        item_id = data['item_id']
        itemObject = item.safe_get_id(item_id=item_id)
        if itemObject is not None:
            print("Item {} already exists in database".format(item_id))
        else:
            name = data['name']
            display_name = data['display_name']
            icon = data['icon']
            recipe = data['recipe']
            description = data['description']
            stats = data['stats']
            tags = data['tags']
            url = data['url']
            set_id = set.safe_get(set_id=float(data['set_id']))

            insert_item = item(
                item_id=item_id,
                name=name,
                display_name=display_name,
                icon=icon,
                description=description,
                stats=stats,
                tags=tags,
                url=url,
                set_id=set_id
            )
            insert_item.save()
            if recipe is not None:
                for items in recipe:
                    item_id = 'TFT_Item_{}'.format(''.join(e for e in items if e.isalnum()))
                    itemObject = item.safe_get_id(item_id=item_id)
                    insert_item.recipe.add(itemObject)

    except ValueError as e:
        print("Item {} input incorrect. Error: {}".format(item_id, e))


def insertUnit(data):
    try:
        name = data['name']
        display_name = data['display_name']
        tier = data['tier']
        traitList = data['trait']
        abilityName = data['ability_name']
        abilityDescription = data['ability_description']
        abilityInfo = data['ability_info']
        abilityIcon = data['ability_icon']
        stats = data['stats']
        icon = data['icon']
        setID = data['set_id']

        unitObject = unit.safe_get_name(name=name, set_id=setID)
        if unitObject is not None:
            print("Unit {} already exists in database".format(name))
        else:
            set_id = set.safe_get(set_id=setID)
            unit_patch = unit(
                name=name,
                display_name=display_name,
                tier=tier,
                ability_name=abilityName,
                ability_description=abilityDescription,
                ability_info=abilityInfo,
                ability_icon=abilityIcon,
                stats=stats,
                icon=icon,
                set_id=set_id
            )
            unit_patch.save()

            for traits in traitList:
                traitName = re.sub(r'[\W_]+', '', traits).lower()
                temp = trait.objects.get(name=traitName, set_id=float(data['set_id']))
                unit_patch.trait.add(temp)

    except ValueError as e:
        print("Unit {} input incorrect. Error: {}".format(name, e))
