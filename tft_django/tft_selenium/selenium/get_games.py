import os
from datetime import timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")

import django
django.setup()

from difflib import SequenceMatcher
from selenium.webdriver.common.by import By
import re

from webdriver_selenium import staleElementLoop
from webdriver_selenium import staleElementLoopByClass

import tft.models
from tft.misc import insertGameUnit
from tft.misc import insertGameTrait
from tft.misc import insertGameInfo
from tft.misc import insertGame
from utils import calculate_date


def getGame(game, playerID):
    gameInfo = {}

    gameID = game.get_attribute("id")

    print('Querying GameID: {}'.format(gameID))

    gameInfo['game_id'] = gameID
    gameInfo['player_id'] = playerID

    if tft.models.game_info.objects.filter(game_id=gameID, player_id=playerID):
        print('Game {} with player {} already exists'.format(gameID, playerID))
        return False

    summary = getGameSummary(game, gameID)
    if not summary:
        return False
    gameInfo['length'] = summary['Length']
    gameInfo['placement'] = summary['Placement']
    gameInfo['level'] = summary['Level']
    gameInfo['round'] = summary['Round']

    insertGameInfo({'game_id': gameID, 'lobby_rank': summary['lobby_rank'], 'queue': summary['Queue'].lower(), 'player_id': playerID})

    try:
        patch = tft.models.patch.objects.filter(date_start__lte=summary['Date'], date_end__gte=summary['Date'])[0]
        patchID = patch.patch_id
        gameInfo['patch_id'] = patchID
    except ObjectDoesNotExist:
        print("No patch found for " + summary['Date'])
        return False

    if summary['Queue'] in ['Ranked', 'Normal', 'Double Up']:
        setID = patch.set_id
    else:
        setID = patch.revival_set_id

    augments = getGameAugments(game, gameID, setID)
    if not augments:
        return False
    gameInfo['augments'] = augments

    headliner, traits = getGameTraits(game, gameID, setID)
    if not (headliner, traits):
        return False
    gameInfo['headliner'] = headliner
    gameInfo['game_traits'] = traits

    units = getGameUnits(game, gameID, patchID, setID)
    if not units:
        return False
    gameInfo['game_units'] = units

    playerGameID = insertGame(gameInfo).pk

    print('Added Game {} of GameID {} with Player {} to database'.format(playerGameID, gameID, playerID))
    return True

def getGameSummary(game, gameID):
    # Get Match Placement
    summaryInfo = {}

    # Specific css element for metatft to find traits
    summaryElement = "#" + gameID + " > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)"

    # Check for StaleElementError, if so return False to skip game
    summaryContainer = staleElementLoop(game, summaryElement, 5)
    if not summaryContainer:
        print("StaleLoopError at Summary")
        return False

    summaryList = summaryContainer.find_elements(By.XPATH, './child::*')

    summaryInfo['Placement'] = int(summaryList[0].text)
    summaryInfo['Queue'] = summaryList[1].text
    summaryInfo['Date'] = calculate_date(summaryList[2].text)
    temp = summaryList[3].text.replace(" • ", " ").split(" ")
    summaryInfo['Length'] = temp[0]
    summaryInfo['Round'] = temp[1]

    if summaryInfo['Queue'] == 'Ranked':
        gameRankSummary = (staleElementLoopByClass(game, 'GameRankSummary', 5)).text.split('\n')
        gameRank = str(gameRankSummary[1] + gameRankSummary[2])
        summaryInfo['lobby_rank'] = gameRank
    else:
        summaryInfo['lobby_rank'] = 'N/A'

    summaryInfo['Level'] = staleElementLoopByClass(game, 'PlayerLevel', 5).text

    print("Got Summary Successfully")
    return summaryInfo

def getGameAugments(game, gameID, setID):
    augmentInfo = []
    augmentElement = "#" + gameID + " > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)"
    augmentContainer = staleElementLoop(game, augmentElement, 5)
    if not augmentContainer:
        print("StaleLoopError at Augments")
        return False

    augmentList = augmentContainer.find_elements(By.CLASS_NAME, 'display-contents')
    if not augmentList:
        return augmentInfo

    for augment in augmentList:
        augmentName = augment.find_element(By.TAG_NAME, 'img').get_attribute('alt')
        augmentName = ''.join(augmentName.split()).lower()
        try:
            temp = tft.models.augment.objects.get(name=augmentName, set_id=setID)
            augmentInfo.append(temp.pk)
        except ObjectDoesNotExist:
            # Uses postgres trigram to find similar words in augment table
            temp = tft.models.augment.objects.filter(name__trigram_strict_word_similar=augmentName, set_id=setID)
            # Checks if more than one similar word is found
            if not temp:
                augmentInfo.append(temp[0].pk)
            else:
                # Uses SequenceMatcher to iterate over temp QuerySet to find the trait that best matches the augment pulled
                # from match based on ratio.
                a = [SequenceMatcher(None, i, augmentName).ratio() for i in temp.values_list('name', flat=False)]
                index = a.index(max(a))
                bestMatch = temp[index]
                augmentInfo.append(bestMatch.pk)
        except Exception as e:
            print("Augment {} not found. Error {}".format(augmentName, e))

    print("Got Augments Successfully")
    return augmentInfo

def getGameTraits(game, gameID, setID):
    traitInfo = []
    headliner = None

    # Specific css element for metatft to find traits
    traitElement = "#" + gameID + " > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)"

    # Check for StaleElementError, if so return False to skip game
    traitContainer = staleElementLoop(game, traitElement, 5)
    if not traitContainer:
        print("StaleLoopError at Augments")
        return False

    traitList = traitContainer.find_elements(By.XPATH, './child::*')
    # Check if player has any traits, if not return an empty list
    if not traitList:
        return traitInfo

    # Query through all traits including headliner
    for trait in traitList:
        if trait.text == '':
            continue

        # Get Headliner
        if trait.get_attribute("class") == "OptionName HeadlinerTraitText":
            headlinerName = re.sub("[^a-zA-Z] ", "", trait.text).replace(' ', '').strip(',').lower()
            headliner = tft.models.trait.objects.get(name=headlinerName, set_id=setID).pk

        numOfTraits = trait.text[0]
        if not numOfTraits.isnumeric():
            continue

        traitName = re.sub("[^a-zA-Z] ", "", trait.text).replace(' ', '').strip(',').lower()
        try:
            temp = tft.models.trait.objects.get(name=traitName, set_id=setID)
            gameTraitID = insertGameTrait({'trait_id': temp, 'count': numOfTraits})
            traitInfo.append(gameTraitID.pk)
        except ObjectDoesNotExist as e:
            print("Trait {} not found. Error {}".format(traitName, e))

    print("Got Headliner and Traits Successfully")
    return headliner, traitInfo


def getGameUnits(game, gameID, patchID, setID):
    unitInfo = []

    # Specific css element for metatft to find units
    unitElement = "#" + gameID + " > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)"

    # Check for StaleElementError, if so return False to skip game
    unitContainer = staleElementLoop(game, unitElement, 5)
    if not unitContainer:
        print("StaleLoopError at Units")
        return False

    unitList = unitContainer.find_elements(By.XPATH, './child::*')
    # Check if player has any units, if not return an empty list
    if not unitList:
        return unitInfo

    for unit in unitList:
        currentUnit = {}

        currentUnit["patch_id"] = patchID
        currentUnit['set_id'] = setID

        # Get Unit Name
        try:
            unitName = unit.find_element(By.CLASS_NAME, 'Unit_img').get_attribute('alt').replace(' ', '').lower()

            #special set10 akali check function
            if unitName == 'akali':
                unitName = checkWhichAkaliSetTen(unit)

            temp = tft.models.unit.objects.get(name=unitName, set_id=setID)
            currentUnit['unit_id'] = temp.pk
        except ObjectDoesNotExist as e:
            print("Unit {} not found. Error {}".format(unitName, e))

        # Get Units Star Level [1,2,3]
        try:
            unitStar = unit.find_element(By.CLASS_NAME, 'Stars_img').get_attribute('alt')
            currentUnit['star'] = (int(re.sub('\D', '', unitStar)))
        except:
            currentUnit['star'] = 1

        itemContainer = unit.find_element(By.CLASS_NAME, 'ItemsContainer')
        itemList = itemContainer.find_elements(By.XPATH, './child::*')
        if not itemContainer:
            currentUnit['items'] = []
            continue

        tempList = []
        for item in itemList:
            itemName = item.find_element(By.CLASS_NAME, 'Item_img').get_attribute('alt')
            itemName = ''.join(itemName.split()).lower()
            try:
                temp = tft.models.item.objects.get(name=itemName, set_id=setID)
                tempList.append(temp.pk)
            except ObjectDoesNotExist as e:
                print("Trait {} not found. Error {}".format(itemName, e))
        currentUnit['items'] = tempList
        gameUnitID = insertGameUnit(currentUnit)
        unitInfo.append(gameUnitID)

    print("Got Units Successfully")
    return unitInfo

def getOtherPlayers(game):
    pass

def checkWhichAkaliSetTen(unit):
    imgURL = unit.find_element(By.CLASS_NAME, 'Unit_img').get_attribute('src')
    if 'truedamage' in imgURL:
        return 'akalitrue-dmg'
    else:
        return 'akalik/da'
