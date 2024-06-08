from django.utils import timezone
from django.db import transaction
from tft.models import account, region, summoner, league, summoner_league, champion_stats, champion_ability
from tft.models import set, patch, trait, trait_effect, champion, item, augment, miscellaneous


def insert_object(model, lookup_params, data_dict):
    try:
        obj, created = model.objects.update_or_create(
            defaults=data_dict,
            **lookup_params
        )
        return obj, created
    except Exception as e:
        raise Exception(f"Error inserting {model.__name__} with lookup {lookup_params}. Error: {e}")


def insertAccount(data):
    try:
        with transaction.atomic():
            account_lookup_params = {'puuid': data['puuid']}
            account_dict = {
                'game_name': data['gameName'],
                'tag_line': data['tagLine'],
            }
            return insert_object(account, account_lookup_params, account_dict)
    except Exception as e:
        raise Exception(f"Error inserting account {data['puuid']}. Error: {e}")


def insertRegion(data):
    try:
        with transaction.atomic():
            region_lookup_params = {'region_id': data['region_id']}
            region_dict = {
                'label': data['label'],
                'server': data['server'],
                'description': data['description'],
            }
            return insert_object(region, region_lookup_params, region_dict)
    except Exception as e:
        raise Exception(f"Error inserting region {data['region_id']}. Error: {e}")


def insertSummoner(data):
    try:
        with transaction.atomic():
            accountObject = account.safe_get_by_puuid(data['puuid'])
            summoner_lookup_params = {'summoner_id': data['id'], 'region': data['region']}
            summoner_dict = {
                'puuid': accountObject,
                'account_id': data['accountId'],
                'icon': data['profileIconId'],
                'level': data['summonerLevel'],
                'last_updated': timezone.now(),
            }
            return insert_object(summoner, summoner_lookup_params, summoner_dict)
    except Exception as e:
        raise Exception(f"Error inserting summoner {data['id']}. Error: {e}")


def insertLeague(data):
    try:
        with transaction.atomic():
            league_lookup_params = {'league_id': data['leagueId'], 'region': data['region']}
            league_dict = {
                'tier': data['tier'],
                'name': data['name'],
                'queue': data['queue']
            }
            return insert_object(league, league_lookup_params, league_dict)
    except Exception as e:
        raise Exception(f"Error inserting league {data['leagueId']}. Error: {e}")


def insertSummonerLeague(data):
    try:
        with transaction.atomic():
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
            return insert_object(summoner_league, summoner_league_lookup_params, summoner_league_dict)
    except Exception as e:
        raise Exception(f"Error inserting SummonerLeague {data['summonerId']}. Error: {e}")


def insertSet(data):
    try:
        with transaction.atomic():
            setID = data['set_id']
            if not set.objects.filter(set_id=setID).exists():
                insert_set = set(
                    set_id=setID,
                    set_name=data['set_name']
                )
                insert_set.save()
    except Exception as e:
        raise Exception(f"Set {setID} input incorrect. Error: {e}")


def insertPatch(data):
    try:
        with transaction.atomic():
            patchID = data['patch_id']
            if not patch.objects.filter(patch_id=patchID).exists():
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
    except Exception as e:
        raise Exception(f"Patch {data['patch_id']} input incorrect. Error: {e}")


def insertTrait(data):
    try:
        with transaction.atomic():
            patch_id = patch.safe_get_patch_id(data['patch_id'])
            api_name = data.get('apiName', f"TFT{int(patch_id.set_id.set_id)}_{data['name']}")
            if not trait.objects.filter(api_name=api_name, patch_id=patch_id).exists():
                insert_trait = trait(
                    api_name=api_name,
                    patch_id=patch_id,
                    display_name=data['name'],
                    description=data['desc'],
                    icon=data['icon'],
                )
                insert_trait.save()
                trait_effects = [
                    trait_effect(
                        trait_id=insert_trait,
                        style=effect.get('style'),
                        min_units=effect['min_units'],
                        max_units=effect['max_units'],
                        variables=effect['variables'],
                    ) for effect in data['effects']
                ]
                trait_effect.objects.bulk_create(trait_effects)
    except Exception as e:
        raise Exception(f"Trait {data['name']} input incorrect. Error: {e}")


def insertChampion(data):
    try:
        with transaction.atomic():
            patch_id = patch.safe_get_patch_id(data['patch_id'])
            api_name = data.get('apiName', f"TFT{int(patch_id.set_id.set_id)}_{data['name']}")
            if not champion.objects.filter(api_name=api_name, patch_id=patch_id).exists():
                insert_champion = champion(
                    api_name=api_name,
                    patch_id=patch_id,
                    character_name=data.get('characterName'),
                    display_name=data['name'],
                    cost=data['cost'],
                    icon=data['icon'],
                    square_icon=data.get('squareIcon'),
                    tile_icon=data.get('tileIcon'),
                )
                insert_champion.save()

                trait_objs = [trait.safe_get_name_patch(i_trait, patch_id) for i_trait in data.get('traits', [])]
                if None in trait_objs:
                    raise ValueError(f"Failed to retrieve one or more traits for champion {data['name']}.")
                insert_champion.trait.add(*filter(None, trait_objs))

                champion_stats.objects.create(
                    champion_id=insert_champion,
                    **data['stats']
                )
                champion_ability.objects.create(
                    champion_id=insert_champion,
                    **data['ability']
                )
    except Exception as e:
        raise Exception(f"Champion {data['name']} input incorrect. Error: {e}")


def insertItem(data):
    try:
        with transaction.atomic():
            patch_id = patch.safe_get_patch_id(data['patch_id'])
            api_name = data.get('apiName', f"TFT{int(patch_id.set_id.set_id)}_{data['name']}")
            if not item.objects.filter(api_name=api_name, patch_id=patch_id).exists():
                insert_item = item(
                    api_name=api_name,
                    patch_id=patch_id,
                    display_name=data['name'],
                    description=data['desc'],
                    icon=data['icon'],
                    unique=data.get('unique', None),
                    effects=data['effects'] if data['effects'] else None,
                    composition=None if data.get('composition') == [] else data.get('composition', None),
                    associated_traits=None if data.get('associatedTraits') == [] else data.get('associatedTraits', None),
                    incompatible_traits=None if data.get('incompatibleTraits') == [] else data.get('incompatibleTraits', None),
                )
                insert_item.save()

                # trait_objs = [trait.safe_get_name_patch(i_trait, patch_id) for i_trait in
                #               data.get('incompatibleTraits', [])]
                # if None in trait_objs:
                #     raise ValueError(f"Failed to retrieve one or more traits for item {data['name']}.")
                # insert_item.incompatible_traits.add(*filter(None, trait_objs))
                #
                # trait_objs = [trait.safe_get_name_patch(i_trait, patch_id) for i_trait in data.get('associatedTraits', [])]
                # if None in trait_objs:
                #     raise ValueError(f"Failed to retrieve one or more traits for item {data['name']}.")
                # insert_item.incompatible_traits.add(*filter(None, trait_objs))

    except Exception as e:
        raise Exception(f"Item {data['name']} input incorrect. Error: {e}")


def insertAugment(data):
    try:
        with transaction.atomic():
            patch_id = patch.safe_get_patch_id(data['patch_id'])
            api_name = data.get('apiName', f"TFT{int(patch_id.set_id.set_id)}_{data['name']}")
            if not augment.objects.filter(api_name=api_name, patch_id=patch_id).exists():
                insert_augment = augment(
                    api_name=api_name,
                    patch_id=patch_id,
                    display_name=data['name'],
                    description=data['desc'],
                    icon=data['icon'],
                    unique=data.get('unique', None),
                    effects=data['effects'] if data['effects'] else None,
                    composition=None if data.get('composition') == [] else data.get('composition', None),
                    associated_traits=None if data.get('associatedTraits') == [] else data.get('associatedTraits', None),
                    incompatible_traits=None if data.get('incompatibleTraits') == [] else data.get('incompatibleTraits', None),
                )
                insert_augment.save()

                # trait_objs = [trait.safe_get_name_patch(i_trait, patch_id) for i_trait in
                #               data.get('incompatibleTraits', [])]
                # if None in trait_objs:
                #     raise ValueError(f"Failed to retrieve one or more traits for augment {data['name']}.")
                # insert_augment.incompatible_traits.add(*filter(None, trait_objs))
                #
                # trait_objs = [trait.safe_get_name_patch(i_trait, patch_id) for i_trait in data.get('associatedTraits', [])]
                # if None in trait_objs:
                #     raise ValueError(f"Failed to retrieve one or more traits for augment {data['name']}.")
                # insert_augment.incompatible_traits.add(*filter(None, trait_objs))

    except Exception as e:
        raise Exception(f"Augment {data['name']} input incorrect. Error: {e}")


def insertMisc(data):
    try:
        with transaction.atomic():
            patch_id = patch.safe_get_patch_id(data['patch_id'])
            api_name = data.get('apiName', f"TFT{int(patch_id.set_id.set_id)}_{data['name']}")
            if not miscellaneous.objects.filter(api_name=api_name, patch_id=patch_id).exists():
                insert_miscellaneous = miscellaneous(
                    api_name=api_name,
                    patch_id=patch_id,
                    display_name=data['name'],
                    description=data['desc'],
                    icon=data['icon'],
                    unique=data.get('unique', None),
                    effects=data['effects'] if data['effects'] else None,
                    composition=None if data.get('composition') == [] else data.get('composition', None),
                    associated_traits=None if data.get('associatedTraits') == [] else data.get('associatedTraits', None),
                    incompatible_traits=None if data.get('incompatibleTraits') == [] else data.get('incompatibleTraits', None),
                )
                insert_miscellaneous.save()

                # trait_objs = [trait.safe_get_name_patch(i_trait, patch_id) for i_trait in data.get('incompatibleTraits', [])]
                # if None in trait_objs:
                #     raise ValueError(f"Failed to retrieve one or more traits for misc {data['name']}.")
                # insert_miscellaneous.incompatible_traits.add(*filter(None, trait_objs))
                #
                # trait_objs = [trait.safe_get_name_patch(i_trait, patch_id) for i_trait in data.get('associatedTraits', [])]
                # if None in trait_objs:
                #     raise ValueError(f"Failed to retrieve one or more traits for misc {data['name']}.")
                # insert_miscellaneous.incompatible_traits.add(*filter(None, trait_objs))

    except Exception as e:
        raise Exception(f"Miscellaneous {data['name']} input incorrect. Error: {e}")
