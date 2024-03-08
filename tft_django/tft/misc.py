from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.utils import IntegrityError

from .models import patch, augment, trait, item, unit, game_unit, set, player, game_info, game, game_trait

def insertPlayer(data):
    try:
        playerName = data['player_name']
        region = data['region']
        lastUpdated = date.today()

        playerID = player.safe_get(playerName=playerName, region=region)

        if playerID is not None:
            print("Player {} already exists in database".format(playerName))
            return playerID.pk

        insert_player = player.objects.create(
            player_name=playerName,
            region=region,
            last_updated=lastUpdated
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
        playerID = data['player_id']
        try:
            gameObject = game_info.objects.get(game_id=gameID)
        except game_info.DoesNotExist:
            gameObject = None

        if gameObject is not None:
            print("Game {} already exists in database, adding player {} to it".format(gameID, playerID))
            #playerObject = player.objects.get(player_id=playerID)
            gameObject.player_id.add(playerID)

        insert_game_info = game_info(
            game_id=gameID,
            lobby_rank=lobbyRank,
            queue=queue
        )
        insert_game_info.save()
        insert_game_info.player_id.add(player.objects.get(player_id=playerID).pk)
        # for players in data['players']:
        #     temp = player.objects.get(player_name=players['player_name'], region=players['region'])
        #     insert_player.player.add(temp)
    except IntegrityError as e:
        print("GameID {} already exists in database. Error: {}".format(gameID, e))
    except ValueError as e:
        print("GameID {} input incorrect. Error: {}".format(gameID, e))

def insertPatch(data):
    if patch.objects.filter(patch_id=data['patch_id'], set_id=float(data['set_id'])).exists():
        print("Patch {} already exists in database".format(data['patch_id']))
        return None
    try:
        set_id = set.objects.get(set_id=float(data['set_id']))
        insert_patch = patch.objects.create(
            patch_id=float(data['patch_id']),
            set_id=set_id,
            date=data['date']
        )
        insert_patch.save()
    except IntegrityError as e:
        print("Patch {} already exists in database. Error: {}".format(data['patch_id'], e))
    except ValueError as e:
        print("Patch {} input incorrect. Error: {}".format(data['patch_id'], e))


def insertAugment(data):
    if augment.objects.filter(name=data['augment_name'], tier=data['tier'], set_id=float(data['set_id'])).exists():
        print("Augment {} already exists in database".format(data['augment_name']))
        return None
    try:
        set_id = set.objects.get(set_id=float(data['set_id']))
        insert_patch = augment.objects.create(
            name=data['augment_name'],
            tier=data['tier'],
            set_id=set_id
        )
        insert_patch.save()
    except IntegrityError as e:
        print("Augment {} already exists in database. Error: {}".format(data['augment_name'], e))
    except ValueError as e:
        print("Augment {} input incorrect. Error: {}".format(data['augment_name'], e))

def insertTrait(data):
    if trait.objects.filter(name=data['trait_name'], set_id=float(data['set_id'])).exists():
        print("Trait {} already exists in database".format(data['trait_name']))
        return None
    try:
        set_id = set.objects.get(set_id=float(data['set_id']))
        insert_patch = trait.objects.create(
            name=data['trait_name'],
            set_id=set_id
        )
        insert_patch.save()
    except IntegrityError as e:
        print("Trait {} already exists in database. Error: {}".format(data['trait_name'], e))
    except ValueError as e:
        print("Trait {} input incorrect. Error: {}".format(data['trait_name'], e))

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
    if item.objects.filter(name=data['item_name'], set_id=float(data['set_id'])).exists():
        print("Item {} already exists in database".format(data['item_name']))
        return None
    try:
        set_id = set.objects.get(set_id=float(data['set_id']))
        insert_patch = item.objects.create(
            name=data['item_name'],
            set_id=set_id
        )
        insert_patch.save()
    except IntegrityError as e:
        print("Item {} already exists in database. Error: {}".format(data['item_name'], e))
    except ValueError as e:
        print("Item {} input incorrect. Error: {}".format(data['item_name'], e))

def insertUnit(data):
    if unit.objects.filter(name=data['unit_name'], set_id=float(data['set_id'])).exists():
        print("Unit {} already exists in database".format(data['unit_name']))
        return None
    try:
        set_id = set.objects.get(set_id=float(data['set_id']))
        unit_patch = unit(
            name=data['unit_name'],
            tier=data['tier'],
            set_id=set_id
        )
        unit_patch.save()
        for traits in data['traits']:
            temp = trait.objects.get(name=traits, set_id=float(data['set_id']))
            unit_patch.trait.add(temp)
    except IntegrityError as e:
        print("Unit {} already exists in database. Error: {}".format(data['unit_name'], e))
    except ValueError as e:
        print("Unit {} input incorrect. Error: {}".format(data['unit_name'], e))

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
        patchID = patch.objects.get(patch_id=data['patch_id'])
        length = data['length']
        placement = data['placement']
        level = data['level']
        round = data['round']
        augmentList = data['augments']
        headliner = data['headliner']
        traitsList = data['game_traits']
        gameUnitsList = data['game_units']

    except Exception as e:
        print("Error in getting game data from parameter. Error: {}".format(e))
        return False

    if game.objects.filter(game_id=gameID, player_id=playerID).exists():
        print("Game {} for player {} already exists in database".format(gameID, playerID))
        return None


    game_patch = game(
        game_id=gameID,
        player_id=playerID,
        patch_id=patchID,
        length=length,
        placement=placement,
        level=level,
        round=round,
    )

    if headliner is not None:
        game_patch.headliner_id = trait.objects.get(trait_id=headliner)

    game_patch.save()

    # Get Augments and Insert to Game
    for augments in augmentList:
        game_patch.augment_id.add(augments)

    for traits in traitsList:
        game_patch.game_trait_id.add(traits)

    for gameUnits in gameUnitsList:
        game_patch.game_unit_id.add(gameUnits)

    return game_patch