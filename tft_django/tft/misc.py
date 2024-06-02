from datetime import date
import re

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.utils import IntegrityError

from .models import patch, augment, trait, item, unit, game_unit, set, player, game_info, game, game_trait, synergy

def insertPlayer(data):
    try:
        playerName = data['player_name']
        region = data['region']
        lastUpdated = data['last_updated']
        icon = data['icon']
        playerRank = data['player_rank']
        playerLP = data['player_lp']

        playerObject = player.safe_get(player_name=playerName, region=region)

        if playerObject is not None:
            if playerObject.icon != icon and icon != "":
                playerObject.icon = icon
            if playerObject.player_rank != playerRank and playerRank != "":
                playerObject.player_rank = playerRank
            if playerObject.player_lp != playerLP:
                playerObject.player_lp = playerLP
            playerObject.save()
            print("Player {} already exists in database".format(playerName))
            return playerObject.pk

        insert_player = player(
            player_name=playerName,
            region=region,
            last_updated=lastUpdated,
            icon=icon,
            player_rank=playerRank,
            player_lp=playerLP
        )
        insert_player.save()
        return insert_player.pk
    except IntegrityError as e:
        print("Player {} already exists in database. Error: {}".format(playerName, e))
    except ValueError as e:
        print("Player {} input incorrect. Error: {}".format(playerName, e))


def insertGameInfo(data):
    try:
        gameID = data['game_id']
        lobbyRank = data['lobby_rank']
        queue = data['queue']
        patchID = patch.objects.get(patch_id=data['patch_id'])
        date = data['date']


        gameObject = game_info.safe_get_game_id(game_id=gameID)

        if gameObject is not None:
            print("Game Info {} already exists in database, querying game first then adding player".format(gameID))
            return gameObject
        else:
            insert_game_info = game_info(
                game_id=gameID,
                lobby_rank=lobbyRank,
                queue=queue,
                patch_id=patchID,
                date=date
            )
            insert_game_info.save()
            return insert_game_info
    except Exception as e:
        print("GameID {} input incorrect. Error: {}".format(gameID, e))

def insertPlayerToGameInfo(data):
    playerID = data['player_id']
    gameInfoObject = data['game_info_object']

    gameInfoObject.player_id.add(player.safe_get_id(player_id=playerID))

def insertSet(data):
    try:
        setID = data['set_id']
        setObject = set.safe_get(set_id=setID)
        if setObject is not None:
            print("Set {} already exists in database".format(setID))
        else:
            setName = data['set_name']

            insert_set = set(
                set_id=setID,
                set_name=setName
            )
            insert_set.save()

    except ValueError as e:
        print("Set {} input incorrect. Error: {}".format(setID, e))


def insertPatch(data):
    try:
        patchID = data['patch_id']
        patchObject = patch.safe_get_patch_id(patch_id=patchID)
        if patchObject is not None:
            print("Patch {} already exists in database".format(data['patch_id']))
        else:
            setID = set.objects.get(set_id=float(data['set_id']))
            dateStart = data['date_start']
            dateEnd = data['date_end']
            highlights = data['highlights']

            insert_patch = patch(
                patch_id=int(patchID),
                set_id=setID,
                date_start=dateStart,
                date_end=dateEnd,
                highlights=highlights
            )
            insert_patch.save()

    except ValueError as e:
        print("Patch {} input incorrect. Error: {}".format(data['patch_id'], e))


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

def insertTrait(data):
    try:
        name = data['name']
        display_name = data['display_name']
        description = data['description']
        synergyList = data['synergy']
        set_id = float(data['set_id'])
        icon = data['icon']
        
        traitObject = trait.safe_get_name(name=name, set_id=set_id)
        if traitObject is not None:
            print("Trait {} already exists in database, skipping".format(name))
        else:    
            set_id = set.objects.get(set_id=float(data['set_id']))
            insert_trait = trait(
                name=name,
                display_name=display_name,
                description=description,
                icon=icon,
                set_id=set_id
            )
            insert_trait.save()
            for synergys in synergyList:
                temp = synergy.objects.get(synergy_id=synergys)
                insert_trait.synergy.add(temp)
                
    except Exception as e:
        print("Trait {} input incorrect. Error: {}".format(name, e))

def insertSynergy(data):
    try:
        name = data['name']
        count = data['count']
        description = data['description']
        set_id = float(data['set_id'])

        synergyObject = synergy.safe_get_by_trait(name=name, count=count, set_id=set_id)
        if synergyObject is not None:
            print("Synergy {} of {} already exists in database, skipping.".format(name, count))
            return synergyObject.pk
        else:
            set_id = set.objects.get(set_id=set_id)
            insert_synergy = synergy(
                name=name,
                count=count,
                description=description,
                set_id=set_id
            )
            insert_synergy.save()
            return insert_synergy.pk
    except Exception as e:
        print("Synergy input incorrect. Error: {}".format(e))


def insertGameTrait(data):
    try:
        traitID = data['trait_id']
        count = data['count']
    except Exception as e:
        print("Error in getting game data from parameter. Error: {}".format(e))
        return False

    if game_trait.objects.filter(trait_id=traitID, count=count).exists():
        print("Trait {} with count {} already exists in database".format(traitID, count))
        return game_trait.objects.get(trait_id=traitID, count=count)

    game_trait_patch = game_trait(
        trait_id=traitID,
        count=count
    )
    game_trait_patch.save()
    return game_trait_patch


def insertItem(data):
    try:
        name = data['name']
        display_name = data['display_name']
        icon = data['icon']
        recipe = data['recipe']
        description = data['description']
        setID = data['set_id']

        itemObject = item.safe_get_name(name=name, set_id=setID)
        if itemObject is not None:
            print("Item {} already exists in database".format(name))

        else:
            set_id = set.safe_get(set_id=setID)
            insert_item = item(
                name=name,
                display_name=display_name,
                icon=icon,
                description=description,
                set_id=set_id
            )
            insert_item.save()
            if recipe is not None:
                for items in recipe:
                    itemObject = item.safe_get_name(name=items, set_id=set_id)
                    insert_item.recipe.add(itemObject)

    except ValueError as e:
        print("Item {} input incorrect. Error: {}".format(itemName, e))

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
        print("Unit {} input incorrect. Error: {}".format(unitName, e))

def insertGameUnit(data):
    try:
        patchID = patch.objects.get(patch_id=float(data['patch_id']))
        set_id = data['set_id']
        unitID = unit.objects.get(unit_id=data['unit_id'], set_id=set_id)
        star = data['star']
        items = data['items']
    except:
        print("Game Unit data incorrect, Error")
        return None

    try:
        existCheck = game_unit.objects.filter(unit_id=unitID, patch_id=patchID, star=star).annotate(count=Count('item')).filter(count=len(items))
        for pk in items:
            existCheck = existCheck.filter(item__pk=pk)
    except:
        print("Error in new filter loop insertGameUnit")
        return None


    if existCheck.exists():
        print("Game Unit {} already exists in database, not creating a new game unit.".format(existCheck))
        return existCheck[0].game_unit_id


    game_unit_patch = game_unit(
        unit_id=unitID,
        patch_id=patchID,
        star=star,
    )
    game_unit_patch.save()

    for items in data['items']:
        try:
            temp = item.objects.get(item_id=items, set_id=set_id)
            game_unit_patch.item.add(temp)
        except ObjectDoesNotExist:
            print("Item {} does not exist in database".format(items))

    return game_unit_patch.pk

def insertGame(data):
    try:
        gameID = game_info.objects.get(game_id=data['game_id'])
        playerID = player.objects.get(player_id=data['player_id'])
        length = data['length']
        placement = data['placement']
        level = data['level']
        round = data['round']
        augmentList = data['augments']
        headliner = data['headliner']
        traitsList = data['game_traits']
        gameUnitsList = data['game_units']
        icon = data['icon']

    except Exception as e:
        print("Error in getting game data from parameter. Error: {}".format(e))
        return False

    if game.objects.filter(game_id=gameID, player_id=playerID).exists():
        print("Game {} for player {} already exists in database".format(gameID, playerID))
        return None


    game_patch = game(
        game_id=gameID,
        player_id=playerID,
        length=length,
        placement=placement,
        level=level,
        round=round,
        icon=icon,
    )

    if headliner is not None:
        game_patch.headliner_id = trait.objects.get(trait_id=headliner)

    game_patch.save()

    # Get Augments and Insert to Game
    for augments in augmentList:
        game_patch.augment_id.add(augments)

    if traitsList is not None:
        for traits in traitsList:
            game_patch.game_trait_id.add(traits)

    for gameUnits in gameUnitsList:
        game_patch.game_unit_id.add(gameUnits)

    return game_patch