import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")
django.setup()

from difflib import SequenceMatcher
from selenium.webdriver.common.by import By
from django.core.exceptions import ObjectDoesNotExist
import re

from webdriver_selenium import staleElementLoop, staleElementLoopByClass, staleElementLoopForClickExpand

import tft.models
from tft.misc import insertGameUnit, insertGameTrait, insertGameInfo, insertGame, insertPlayer, insertPlayerToGameInfo
from utils import calculate_date


def getGame(game, playerID):
    gameInfo = {}
    gameID = game.get_attribute("id")
    print('Querying GameID: {}'.format(gameID))
    gameInfo['game_id'] = gameID
    gameInfo['player_id'] = playerID

    # # Check if player_id with game_id exists in database, if so, return false to skip game
    #Moved to tft_query.py
    # if tft.models.game_info.objects.filter(game_id=gameID, player_id=playerID):
    #     print('Game {} with player {} already exists'.format(gameID, playerID))
    #     return False

    # Click Expand Button for Each Game
    expandElement = "#" + gameID + " > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > svg:nth-child(1)"
    staleElementLoopForClickExpand(game, expandElement, 5)

    # Summary Section
    # Get summary of the game, calling getGameSummary function
    summary = getGameSummary(game, gameID)
    if not summary:
        print("Error in get_games.py, summary section")
        return False
    gameInfo['length'] = summary['Length']
    gameInfo['placement'] = summary['Placement']
    gameInfo['level'] = summary['Level']
    gameInfo['round'] = summary['Round']
    gameInfo['date'] = summary['Date']

    # Get Patch from game date
    try:
        patch = tft.models.patch.objects.get(date_start__lte=summary['Date'], date_end__gte=summary['Date'])
        patchID = patch.patch_id
        gameInfo['patch_id'] = patchID
    except ObjectDoesNotExist:
        print("Patch for date {} not found".format(str(summary['Date'])))
        return False

    # GameInfo section
    gameInfoObject = insertGameInfo(
        {'game_id': gameID, 'lobby_rank': summary['lobby_rank'], 'queue': summary['Queue'],
         "player_id": playerID, 'date': summary['Date'], 'patch_id': patchID})
    if gameInfoObject is None:
        print("Error in get_games.py, gameinfo section")
        return False


    if summary['Queue'] in ['Ranked', 'Normal', 'Double Up', 'Hyper Roll']:
        setID = patch.set_id
    else:
        setID = patch.revival_set_id


    gameInfo['icon'] = staleElementLoopByClass(game, 'TacticianPortait', 5).get_attribute('src')


    # Augments Section
    augments = getGameAugments(game, gameID, setID)
    if not augments:
        print("Error in get_games.py, augments section")
        return False
    gameInfo['augments'] = augments


    # Trait Section
    traits, headliner = getGameTraits(game, gameID, setID)
    if not traits:
        print("Error in get_games.py, trait section")
        return False
    gameInfo['headliner'] = headliner
    gameInfo['game_traits'] = traits

    # Unit Section
    units = getGameUnits(game, gameID, patchID, setID)
    if not units:
        print("Error in get_games.py, units section")
        return False
    gameInfo['game_units'] = units

    # Game Section
    playerGameObject = insertGame(gameInfo)
    if playerGameObject is None:
        print("in get_games.py, game section, unable to add game")
        return False
    playerGameID = playerGameObject.pk
    insertPlayerToGameInfo({"player_id": playerID, "game_info_object": gameInfoObject})
    print('Added Game {} of GameID {} with Player {} to database'.format(playerGameID, gameID, playerID))


    # Get Other Players in Game
    print('Now getting sub-players of the game')
    getOtherPlayers(game)
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
        gameRankSummary = (staleElementLoopByClass(game, 'GameRankSummary', 3))
        if not gameRankSummary:
            summaryInfo['lobby_rank'] = 'N/A'
        else:
            gameRankSummary = gameRankSummary.text.split('\n')
            gameRank = str(gameRankSummary[1] + ' ' + gameRankSummary[2])
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
        augmentName = re.sub('[^a-zA-Z+]+', '', augmentName).lower()
        try:
            temp = tft.models.augment.objects.get(name=augmentName, set_id=setID)
            augmentInfo.append(temp.pk)
        except ObjectDoesNotExist:
            # Uses postgres trigram to find similar words in augment table
            temp = tft.models.augment.objects.filter(name__trigram_strict_word_similar=augmentName, set_id=setID)
            # Checks if more than one similar word is found
            if not temp:
                return False
                # print(augmentInfo)
                # augmentInfo.append(temp[0].pk)
            elif len(temp) == 0:
                return False
            else:
                # Uses SequenceMatcher to iterate over temp QuerySet to find the trait that best matches the augment pulled
                # from match based on ratio.
                a = [SequenceMatcher(None, i, augmentName).ratio() for i in temp.values_list('name', flat=False)]
                index = a.index(max(a))
                bestMatch = temp[index]
                augmentInfo.append(bestMatch.pk)
            print(augmentInfo)
        except Exception as e:
            print("Augment {} not found. Error {}".format(augmentName, e))
            return False
    print("Got Augments Successfully")
    return augmentInfo


def getGameTraits(game, gameID, setID):
    traitInfo = []
    headliner = None

    # Specific css element for metatft to find traits
    traitElement = "#" + gameID + " > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)"

    # Check for StaleElementError, if so return False to skip game
    traitContainer = staleElementLoop(game, traitElement, 5)
    if not traitContainer or traitContainer is None:
        print("StaleLoopError at Augments")
        return None, None

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
            headlinerName = re.sub('[^a-zA-Z]+', "", trait.text).lower()
            headliner = tft.models.trait.safe_get_name(name=headlinerName, set_id=setID)
            if headliner is not None:
                headliner = headliner.pk

        numOfTraits = trait.text[0]
        if not numOfTraits.isnumeric():
            continue

        traitName = re.sub('[^a-zA-Z]+', "", trait.text).lower()
        temp = tft.models.trait.safe_get_name(name=traitName, set_id=setID)
        if temp is None:
            continue
        gameTraitID = insertGameTrait({'trait_id': temp, 'count': numOfTraits})
        traitInfo.append(gameTraitID.pk)

    print("Got Headliner and Traits Successfully")
    return traitInfo, headliner


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
            unitName = unit.find_element(By.CLASS_NAME, 'Unit_img').get_attribute('alt')
            unitName = re.sub('[^a-zA-Z]+', '', unitName).lower()

            # special set10 akali check function
            # if unitName == 'akali':
            #     unitName = checkWhichAkaliSetTen(unit)

            # special set 11 kayle check
            if unitName == 'kayle':
                continue

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
            itemName = re.sub('[^a-zA-Z+]+', '', itemName).lower()
            try:
                temp = tft.models.item.objects.get(name=itemName, set_id=setID)
                tempList.append(temp.pk)
            except ObjectDoesNotExist:
                # Uses postgres trigram to find similar words in item table
                temp = tft.models.item.objects.filter(name__trigram_strict_word_similar=itemName, set_id=setID)
                # Checks if more than one similar word is found
                if len(temp) == 0:
                    return False
                elif len(temp) == 1:
                    tempList.append(temp[0].pk)
                else:
                    # Uses SequenceMatcher to iterate over temp QuerySet to find the trait that best matches the item pulled
                    # from match based on ratio.
                    a = [SequenceMatcher(None, i, itemName).ratio() for i in temp.values_list('name', flat=False)]
                    index = a.index(max(a))
                    bestMatch = temp[index]
                    tempList.append(bestMatch.pk)
            except Exception as e:
                print("Item {} not found. Error {}".format(itemName, e))

        currentUnit['items'] = tempList
        gameUnitID = insertGameUnit(currentUnit)
        unitInfo.append(gameUnitID)

    print("Got Units Successfully")
    return unitInfo


def getOtherPlayers(game):
    playerCSSSelector = ".PlayerGameList"
    playersContainer = staleElementLoop(game, playerCSSSelector, 5)
    playersList = playersContainer.find_elements(By.XPATH, './child::*')
    for players in playersList:
        playerLink = players.find_element(By.CLASS_NAME, 'PlayerMatchName').get_attribute('href')
        if playerLink is None:
            continue
        region = playerLink[31:33]
        playerName = playerLink[34:]
        insertPlayer({'player_name': playerName, 'region': region, "last_updated": None, 'icon': '', 'player_rank': '',
                      'player_lp': 0})

# Special akali check for set 10, as it was named akali(akali kda) and akalitruedamage
def checkWhichAkaliSetTen(unit):
    imgURL = unit.find_element(By.CLASS_NAME, 'Unit_img').get_attribute('src')
    if 'truedamage' in imgURL:
        return 'akalitruedmg'
    else:
        return 'akalikda'
