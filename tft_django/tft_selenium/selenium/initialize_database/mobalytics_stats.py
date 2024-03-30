from selenium.webdriver.common.by import By
import re

from webdriver_selenium import loadPage, staleElementLoop, quickLoadPage

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")
django.setup()

from tft.misc import insertAugment, insertTrait, insertUnit, insertItem, insertSet

def mobalyticsQuery(url):
    browser = loadPage(url)

    setName = staleElementLoop(browser, '.m-1f0cxht', 5).text
    setNumber = re.search(r"[-+]?\d*\.*\d+", setName).group(0)

    container = staleElementLoop(browser, ".m-d7kr9k", 5)
    dataList = container.find_elements(By.XPATH, './child::*')[1:]

    return dataList, setNumber

def mobalyticsChampionPage(url):
    browser = quickLoadPage(url)
    traitList = []

    container = staleElementLoop(browser, '.m-ybmp4j', 5)
    traits = container.find_elements(By.CSS_SELECTOR, '.m-1jj7hqe')
    for trait in traits:
        traitName = re.sub('[^a-zA-Z+]+','', trait.text).lower()
        traitList.append(traitName)

    return traitList

def loadSet(url):
    browser = quickLoadPage(url)
    setName = staleElementLoop(browser, '.m-1f0cxht', 5).text
    setNumber = re.search(r"[-+]?\d*\.*\d+", setName).group(0)

    if setNumber is float:
        setType = "Revival"
    else:
        setType = "Main"

    insertSet({'set_id': setNumber, 'set_name': setName, 'set_type': setType})
    print("Set loaded")

def loadAugments(url, debug_mode=False):
    print("Loading augments...")
    augmentList, setNumber = mobalyticsQuery(url)
    for augment in augmentList:
        augmentInfo = augment.text.split("\n")
        augmentName = re.sub('[^a-zA-Z+]+', '', augmentInfo[1]).lower()
        if debug_mode:
            print(augmentInfo)
        else:
            insertAugment({'augment_name': augmentName, 'set_id': setNumber})
    print("Augments loaded")

def loadTraits(url, debug_mode=False):
    print("Loading traits...")
    traitList, setNumber = mobalyticsQuery(url)
    for trait in traitList:
        traitInfo = trait.text.split("\n")
        traitName = re.sub('[^a-zA-Z+]+', '', traitInfo[1]).lower()
        if debug_mode:
            print(traitInfo)
        else:
            insertTrait({'trait_name': traitName, 'set_id': setNumber})
    print("Traits loaded")

def loadItems(url, debug_mode=False):
    print("Loading items...")
    itemList, setNumber = mobalyticsQuery(url)
    for item in itemList:
        itemInfo = item.text.split("\n")
        itemName = re.sub('[^a-zA-Z+]+', '', itemInfo[1]).lower()
        if debug_mode:
            print(itemInfo)
        else:
            insertItem({'item_name': itemName, 'set_id': setNumber})
    print("Items loaded")


def loadUnits(url, debug_mode=False):
    print("Loading units...")
    unitList, setNumber = mobalyticsQuery(url)
    for unit in unitList:
        unitInfo = unit.text.split("\n")
        unitName = re.sub('[^a-zA-Z+]+', '', unitInfo[1]).lower()
        unitLink = staleElementLoop(unit, '.m-uj7l7m', 5).get_attribute('href')
        traits = mobalyticsChampionPage(unitLink)
        if debug_mode:
            print(unitName)
            print(traits)
        else:
            insertUnit({'unit_name': unitName, 'set_id': setNumber, 'traits': traits})
    print("Units loaded")


mobalytics_url = "https://mobalytics.gg/tft"
augments_url = "https://mobalytics.gg/tft/tier-list/augments"
traits_url = "https://mobalytics.gg/tft/tier-list/traits"
items_url = "https://mobalytics.gg/tft/tier-list/items"
units_url = "https://mobalytics.gg/tft/tier-list/champions"

loadSet(mobalytics_url)
loadAugments(augments_url)
loadItems(items_url)
loadTraits(traits_url)
loadUnits(units_url)



