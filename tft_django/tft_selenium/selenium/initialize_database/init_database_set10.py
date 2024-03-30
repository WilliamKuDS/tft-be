import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")

import django
django.setup()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tft.misc import insertAugment
from tft.misc import insertTrait
from tft.misc import insertUnit
from tft.misc import insertItem

from webdriver_selenium import loadPage
from webdriver_selenium import staleElementLoop

import re

def mobalyticsLoad(url, css_selector):
    browser = loadPage(url)
    wait = WebDriverWait(browser, timeout=5)

    container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    dataList = container.find_elements(By.XPATH, './child::*')
    setName = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.m-1f0cxht'))).text
    setNumber = float(re.search(r"[-+]?(?:\d.\d+)", setName).group())

    return dataList, setNumber
def loadAugments(url):
    augmentList, setNumber = mobalyticsLoad(url, '.m-101th0h')
    for augment in augmentList[1:]:
        augmentInfo = augment.text.split("\n")
        insertAugment({'augment_name': ''.join(augmentInfo[0].split()).lower(), 'tier': int(augmentInfo[1]), 'set_id': setNumber})
    print("Augments loaded")

def loadTraits(url):
    traitList, setNumber = mobalyticsLoad(url, '.m-5qjqaf')
    for trait in traitList:
        traitInfo = trait.text.split("\n")
        insertTrait({'trait_name': ''.join(traitInfo[0].split()).lower(), 'set_id': setNumber})
    print("Traits loaded")

def loadItems(url):
    itemList, setNumber = mobalyticsLoad(url, '.m-5vhgcj')
    for item in itemList[4:]:
        itemInfo = item.text.split("\n")
        insertItem({'item_name': ''.join(itemInfo[0].split()).lower(), 'set_id': setNumber})
    print("Items loaded")


def loadUnits(url):
    championList, setNumber = mobalyticsLoad(url, '.m-1o47yso')
    for champion in championList:
        championInfo = champion.text.split("\n")
        if len(championInfo) == 4:
            traits = [''.join(championInfo[0].split()).lower(), ''.join(championInfo[1].split()).lower()]
            insertUnit({'unit_name': ''.join(championInfo[2].split()).lower(), 'tier': int(championInfo[3]), 'set_id': setNumber, 'traits': traits})
        if len(championInfo) == 5:
            traits = [''.join(championInfo[0].split()).lower(), ''.join(championInfo[1].split()).lower(), ''.join(championInfo[2].split()).lower()]
            insertUnit({'unit_name': ''.join(championInfo[3].split()).lower(), 'tier': int(championInfo[4]), 'set_id': setNumber, 'traits': traits})
    print("Units loaded")



# Set 10 Links
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
items_url = [items_basic_url, items_combined_url, items_artifact_url, items_support_url, items_noncraft_url, items_radiant_url]

units_url = "https://mobalytics.gg/tft/champions"

for url in augment_url:
    loadAugments(url)

for url in traits_url:
    loadTraits(url)

for url in items_url:
    loadItems(url)

loadUnits(units_url)

# Set 3.5 Links
augment_1_url = "https://mobalytics.gg/tft/set3-5/augments?tier=1"
augment_2_url = "https://mobalytics.gg/tft/set3-5/augments?tier=2"
augment_3_url = "https://mobalytics.gg/tft/set3-5/augments?tier=3"
augment_url = [augment_1_url, augment_2_url, augment_3_url]

traits_origin_url = "https://mobalytics.gg/tft/set3-5/synergies/origins"
traits_classes_url = "https://mobalytics.gg/tft/set3-5/synergies/classes"
traits_url = [traits_origin_url, traits_classes_url]

items_basic_url = "https://mobalytics.gg/tft/set3-5/items"
items_combined_url = "https://mobalytics.gg/tft/set3-5/items/combined"
items_artifact_url = "https://mobalytics.gg/tft/set3-5/items/ornns"
items_support_url = "https://mobalytics.gg/tft/set3-5/items/support"
items_noncraft_url = "https://mobalytics.gg/tft/set3-5/items/elusive"
items_radiant_url = "https://mobalytics.gg/tft/set3-5/items/radiant"
items_url = [items_basic_url, items_combined_url, items_artifact_url, items_support_url, items_noncraft_url, items_radiant_url]

units_url = "https://mobalytics.gg/tft/set3-5/champions"

for url in augment_url:
    loadAugments(url)

for url in traits_url:
    loadTraits(url)

for url in items_url:
    loadItems(url)

loadUnits(units_url)

