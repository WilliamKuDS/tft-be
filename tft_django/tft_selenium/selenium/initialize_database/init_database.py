import os
import time

from dateutil import parser

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")
import django

django.setup()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tft.misc import insertAugment, insertTrait, insertUnit, insertItem, insertSet, insertSynergy
from tft_selenium.selenium.webdriver_selenium import loadPage, staleElementLoop, quickLoadPage, staleElementLoopByXPath

import re


# pack lamps

def mobalyticsLoad(url, css_selector):
    browser = loadPage(url)
    wait = WebDriverWait(browser, timeout=5)
    time.sleep(1)

    container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    dataList = container.find_elements(By.XPATH, './child::*')
    setName = staleElementLoop(browser, '.m-1f0cxht', 5).text
    setNumber = re.search(r"[-+]?\d*\.*\d+", setName).group(0)
    return browser, dataList, setNumber


def mobalyticsChampionPage(url):
    browser = quickLoadPage(url)

    unitContainer = staleElementLoop(browser, '.m-1rxgvzo', 5)
    unitMain = unitContainer.find_element(By.CLASS_NAME, 'm-ybmp4j').text.split('\n')
    unitAbility = unitContainer.find_element(By.CLASS_NAME, 'm-jknwuc').text.split('\n')
    abilityIcon = unitContainer.find_element(By.CLASS_NAME, 'm-li4udt').get_attribute('src')
    unitStats = unitContainer.find_element(By.CLASS_NAME, 'm-f5iy9m').text.split('\n')
    browser.quit()

    return unitMain, unitAbility, abilityIcon, unitStats


def loadSet(url):
    browser = quickLoadPage(url)
    setName = staleElementLoop(browser, '.m-1f0cxht', 5).text
    setNumber = re.search(r"[-+]?\d*\.*\d+", setName).group(0)

    if setNumber is float:
        setType = "Revival"
    else:
        setType = "Main"

    insertSet({
        'set_id': setNumber,
        'set_name': setName,
        'set_type': setType
    })
    browser.quit()
    print("Set loaded")


def loadAugments(url):
    browser, augmentList, setNumber = mobalyticsLoad(url, '.m-101th0h')
    for augment in augmentList:
        if augment.get_attribute('class') not in ['m-1uum3g8']:
            continue
        augmentInfo = augment.text.split("\n")
        #augmentIcon = augment.find_element(By.CLASS_NAME, 'm-1kiugpc').get_attribute('src')
        augmentIcon = staleElementLoop(augment, '.m-1kiugpc', 5)
        if not augmentIcon or augmentIcon is None:
            augmentIcon = None
        else:
            augmentIcon = augmentIcon.get_attribute('src')
        insertAugment({
            'name': re.sub('[^a-zA-Z+]+', '', augmentInfo[0]).lower(),
            'display_name': augmentInfo[0],
            'set_id': setNumber,
            'tier': augmentInfo[1],
            'icon': augmentIcon,
            'description': augmentInfo[2]
        })
        browser.execute_script("window.scrollBy(0, 200)")
    browser.quit()
    print("Augments loaded")


def loadTraits(url):
    browser, traitList, setNumber = mobalyticsLoad(url, '.m-5qjqaf')
    for trait in traitList:
        traitInfo = trait.find_element(By.CLASS_NAME, 'm-1ry2ldu.e153f6yx2').text.splitlines()
        traitName = re.sub(r'[\W_]+', '', traitInfo[0]).lower()
        displayName = traitInfo[0]
        traitDescription = traitInfo[1]
        traitIcon = trait.find_element(By.CLASS_NAME, 'm-8k2h0n').get_attribute('src')
        traitSynergy = trait.find_element(By.CLASS_NAME, 'm-1u6yqqf.e153f6yx1').text.splitlines()
        synergyList = []
        for i in range(0, len(traitSynergy), 2):
            synergyCount = traitSynergy[i]
            synergyDescription = traitSynergy[i + 1]
            synergyID = insertSynergy({
                'name': traitName,
                'count': synergyCount,
                'description': synergyDescription,
                'set_id': setNumber
            })
            synergyList.append(synergyID)
        insertTrait({
            'name': traitName,
            'display_name': displayName,
            'description': traitDescription,
            'synergy': synergyList,
            'icon': traitIcon,
            'set_id': setNumber
        })
        browser.execute_script("window.scrollBy(0, 200)")
    browser.quit()
    print("Traits loaded")


def loadItems(url):
    browser, itemList, setNumber = mobalyticsLoad(url, '.m-5vhgcj')
    for item in itemList:
        if item.get_attribute('class') not in ['m-1ogd70h e76wflj5', 'm-jbp8l2 e5d3hmh5', 'm-w9ejib']:
            continue
        itemInfo = item.text.split("\n")
        itemIcon = staleElementLoopByXPath(item, './div[1]/img', 5)
        if not itemIcon or itemIcon is None:
            itemIcon = None
        else:
            itemIcon = itemIcon.get_attribute('src')
        recipe = item.find_elements(By.CLASS_NAME, 'e5d3hmh0.m-1jcejho')
        if len(recipe) == 2:
            recipe_item_one = re.sub('[^a-zA-Z+]+', '', recipe[0].get_attribute('alt')).lower()
            recipe_item_two = re.sub('[^a-zA-Z+]+', '', recipe[1].get_attribute('alt')).lower()
            insertItem({
                'name': re.sub('[^a-zA-Z+]+', '', itemInfo[0]).lower(),
                'display_name': itemInfo[0],
                'icon': itemIcon,
                'recipe': [recipe_item_one, recipe_item_two],
                'description': itemInfo[1],
                'set_id': setNumber
            })
        else:
            insertItem({
                'name': re.sub('[^a-zA-Z+]+', '', itemInfo[0]).lower(),
                'display_name': itemInfo[0],
                'icon': itemIcon,
                'recipe': None,
                'description': itemInfo[1],
                'set_id': setNumber
            })
            browser.execute_script("window.scrollBy(0, 200)")
    browser.quit()
    print("Items loaded")


def loadUnits(url):
    browser, unitList, setNumber = mobalyticsLoad(url, '.m-1o47yso')
    for unit in unitList:
        unitIcon = str(unit.find_element(By.CLASS_NAME, 'm-2ni1l0').get_attribute('style')[23:-3])
        unitURL = unit.get_attribute('href')
        unitMain, unitAbility, abilityIcon, unitStats = mobalyticsChampionPage(unitURL)
        unitName = re.sub(r'[\W_]+', '', str(unitMain[-2])).lower()
        displayName = str(unitMain[-2])
        unitTier = int(unitMain[-1])
        unitTraits = unitMain[:-2]
        abilityName = str(unitAbility[1])
        abilityDescription = str(unitAbility[2])
        abilityInfo = unitAbility[3:]
        unitStats = unitStats[1:-1]

        insertUnit({
            'name': unitName,
            'display_name': displayName,
            'tier': unitTier,
            'trait': unitTraits,
            'ability_name': abilityName,
            'ability_description': abilityDescription,
            'ability_info': abilityInfo,
            'ability_icon': abilityIcon,
            'stats': unitStats,
            'icon': unitIcon,
            'set_id': setNumber
        })
        print("Loaded unit {}".format(unitName))
        browser.execute_script("window.scrollBy(0, 200)")
    browser.quit()
    print("Units loaded")


# def loadPatch(url):
#     browser = loadPage(url)
#     patchTable = staleElementLoop(browser, '.style__List-sc-106zuld-2', 5)
#     patchList = patchTable.find_elements(By.XPATH, './child::*')
#     for patches in patchList:
#         patchID = patches.text.split('\n')[1].split(' ')[3]
#         date = patches.find_element(By.CSS_SELECTOR, 'a:nth-child(1) > article:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > time:nth-child(2)').get_attribute('datetime')
#         date = str(parser.isoparse(date)).split(' ')[0]
#         print(date)
#     browser.close()


patch_url = "https://www.leagueoflegends.com/en-us/news/tags/teamfight-tactics-patch-notes/"
# Set 10 Links
main_url = "https://mobalytics.gg/tft"

augment_1_url = "https://mobalytics.gg/tft/augments?tier=1"
augment_2_url = "https://mobalytics.gg/tft/augments?tier=2"
augment_3_url = "https://mobalytics.gg/tft/augments?tier=3"
augment_url = [augment_1_url, augment_2_url, augment_3_url]

traits_origin_url = "https://mobalytics.gg/tft/synergies/origins"
traits_classes_url = "https://mobalytics.gg/tft/synergies/classes"
traits_url = [traits_origin_url, traits_classes_url]

items_basic_url = "https://mobalytics.gg/tft/items"
items_combined_url = "https://mobalytics.gg/tft/items/combined"
items_artifact_url = "https://mobalytics.gg/tft/items/ornns"
items_support_url = "https://mobalytics.gg/tft/items/support"
items_noncraft_url = "https://mobalytics.gg/tft/items/elusive"
items_radiant_url = "https://mobalytics.gg/tft/items/radiant"
items_url = [items_basic_url, items_combined_url, items_artifact_url, items_support_url, items_noncraft_url,
             items_radiant_url]

units_url = "https://mobalytics.gg/tft/champions"

loadSet(main_url)
for url in augment_url:
    loadAugments(url)

for url in traits_url:
    loadTraits(url)

for url in items_url:
    loadItems(url)

loadUnits(units_url)

# # Set 3.5 Links
# main_url = "https://mobalytics.gg/tft/set3-5"
# augment_1_url = "https://mobalytics.gg/tft/set3-5/augments?tier=1"
# augment_2_url = "https://mobalytics.gg/tft/set3-5/augments?tier=2"
# augment_3_url = "https://mobalytics.gg/tft/set3-5/augments?tier=3"
# augment_url = [augment_1_url, augment_2_url, augment_3_url]
#
# traits_origin_url = "https://mobalytics.gg/tft/set3-5/synergies/origins"
# traits_classes_url = "https://mobalytics.gg/tft/set3-5/synergies/classes"
# traits_url = [traits_origin_url, traits_classes_url]
#
# items_basic_url = "https://mobalytics.gg/tft/set3-5/items"
# items_combined_url = "https://mobalytics.gg/tft/set3-5/items/combined"
# items_artifact_url = "https://mobalytics.gg/tft/set3-5/items/ornns"
# items_support_url = "https://mobalytics.gg/tft/set3-5/items/support"
# items_noncraft_url = "https://mobalytics.gg/tft/set3-5/items/elusive"
# items_radiant_url = "https://mobalytics.gg/tft/set3-5/items/radiant"
# items_url = [items_basic_url, items_combined_url, items_artifact_url, items_support_url, items_noncraft_url, items_radiant_url]

# units_url = "https://mobalytics.gg/tft/set3-5/champions"

# loadSet(main_url)

# for url in augment_url:
#     loadAugments(url)
#
# for url in traits_url:
#     loadTraits(url)
#
# for url in items_url:
#     loadItems(url)
#
# loadUnits(units_url)

# loadPatch(patch_url)
