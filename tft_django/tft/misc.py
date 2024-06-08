from datetime import date
import re

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils import timezone

from tft.models import account, region, summoner, league, summoner_league, champion_stats, champion_ability
from tft.models import set, patch, trait, trait_effect, champion, item, augment


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
        summonerObject = summoner.safe_get_by_summoner_id_region(data['summonerId'], data['region'])
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
        if setObject is None:
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
        if patchObject is None:
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
        if traitObject is None:
            insert_trait = trait(
                api_name=api_name,
                patch_id=patch_id,
                display_name=data['name'],
                description=data['desc'],
                icon=data['icon'],
            )
            insert_trait.save()

            for effect in data['effects']:
                style = effect['style'] if 'style' in data else None

                insert_trait_effect = trait_effect(
                    trait_id=insert_trait,
                    style=style,
                    min_units=effect['min_units'],
                    max_units=effect['max_units'],
                    variables=data['variables'],
                )
                insert_trait_effect.save()

    except Exception as e:
        raise Exception("Trait {} input incorrect. Error: {}".format(data, e))

def insertChampion(data):
    try:
        patch_id = patch.safe_get_patch_id(data['patch_id'])
        if 'apiName' in data:
            api_name = data['apiName']
        else:
            api_name = 'TFT' + str(int(patch_id.set_id.set_id)) + '_' + data['name']

        championObject = champion.safe_get_api_name_patch(api_name=api_name, patch_id=patch_id)
        if championObject is None:
            character_name = data['characterName'] if 'champion' in data else None
            square_icon = data['squareIcon'] if 'squareIcon' in data else None
            tile_icon = data['tileIcon'] if 'tileIcon' in data else None

            insert_champion = champion(
                api_name=api_name,
                patch_id=patch_id,
                character_name=character_name,
                display_name=data['name'],
                cost=data['cost'],
                icon=data['icon'],
                square_icon=square_icon,
                tile_icon=tile_icon,
            )
            insert_champion.save()

            for curr_trait in data['traits']:
                traitObject = trait.safe_get_name_patch(curr_trait, patch_id)
                if traitObject is not None:
                    insert_champion.trait.add(traitObject)
                else:
                    raise Exception("Trait {} input incorrect or doesn't exist in database. Error: {}".format(trait, patch_id))

            insert_champion_stats = champion_stats(
                champion_id=insert_champion,
                armor=data['stats']['armor'],
                attack_speed=data['stats']['attackSpeed'],
                crit_chance=data['stats']['critChance'],
                crit_multiplier=data['stats']['critMultiplier'],
                damage=data['stats']['damage'],
                hp=data['stats']['hp'],
                initial_mana=data['stats']['initialMana'],
                magic_resist=data['stats']['magicResist'],
                mana=data['stats']['mana'],
                range=data['stats']['range']
            )
            insert_champion_stats.save()

            insert_champion_ability = champion_ability(
                champion_id=insert_champion,
                description=data['ability']['desc'],
                icon=data['ability']['icon'],
                name=data['ability']['name'],
                variables=data['ability']['variables'],
            )
            insert_champion_ability.save()

    except Exception as e:
        raise Exception("Champion {} input incorrect. Error: {}".format(api_name, e))

def insertAugment(data):
    pass

def insertItem(data):
    pass

def insertMisc(data):
    pass