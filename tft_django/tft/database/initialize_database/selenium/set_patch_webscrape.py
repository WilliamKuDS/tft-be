from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
import re
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")
django.setup()

from tft.misc import insertSet, insertPatch


def webscrape_set_data(browser):
    wait = WebDriverWait(browser, timeout=5)
    expand_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mw-parser-output')))
    expand_box.find_element(By.TAG_NAME, 'a').click()

    container = browser.find_element(By.CSS_SELECTOR, "table.navbox.hlist")
    set_table = container.find_elements(By.XPATH, './tbody/child::*')
    set_id_list = []

    for curr_set in set_table:
        set_patch_dict = {}
        set_text = curr_set.text.splitlines()[0]

        if 'Upcoming' in set_text:
            continue

        set_info = set_text.split(':', 1)
        set_id = float(set_info[0].strip(' Set '))
        set_patch_dict['set_id'] = set_id
        set_patch_dict['set_name'] = set_info[1].strip()
        insertSet(set_patch_dict)
        set_id_list.append(set_id)

    return set_id_list


def iterate_thru_patches_urls_from_set_ids(set_id_list, browser):
    final_patch_list = []

    for set_id in set_id_list:
        if set_id == 5.5:
            continue

        set_id_url = convert_float_to_int(set_id)
        browser.get(f"https://leagueoflegends.fandom.com/wiki/Category:Set_{set_id_url}_patch_notes")
        patch_elements = browser.find_elements(By.CSS_SELECTOR, 'a.category-page__member-link')
        patch_urls = [element.get_attribute('href') for element in patch_elements]

        patch_list = [
            result
            for patch in patch_urls
            if (result := webscrape_patch_data(patch, set_id, browser)) is not None
        ]

        final_patch_list.extend(sorted(patch_list, key=lambda x: patch_key(x['patch_id']), reverse=True))

    save_patch_list_to_db(final_patch_list)


def webscrape_patch_data(patch_page_url, set_id, browser):
    browser.get(patch_page_url)
    patch_dict = {'set_id': set_id}

    patch_info_container = browser.find_element(By.TAG_NAME, 'aside')
    patch_id = patch_info_container.find_element(By.TAG_NAME, 'h2').text.split(' ')[0].strip('V')

    if 'b' in patch_id:
        return None

    if set_id == 5.0:
        patch_dict['set_id'] = special_case_for_set_five_because_people_who_manage_websites_hate_us(patch_id)

    patch_dict['patch_id'] = patch_id
    patch_info = patch_info_container.find_elements(By.TAG_NAME, 'section')

    patch_date_unformatted = patch_info[0].text.splitlines()[1]
    match = re.match(r'(\w+)\s(\d+)[a-z]{2},\s(\d{4})', patch_date_unformatted)

    if not match:
        raise ValueError("Date string format is incorrect")

    month, day, year = match.groups()
    patch_dict['date_start'] = datetime.strptime(f"{month} {day}, {year}", "%B %d, %Y").date()
    patch_dict['highlights'] = patch_info[1].text.splitlines()[1:]
    patch_dict['patch_url'] = patch_info[2].find_element(By.TAG_NAME, 'a').get_attribute('href')

    return patch_dict


def save_patch_list_to_db(patch_list):
    prev_date = None
    for patch in patch_list:
        patch['date_end'] = prev_date - timedelta(days=1) if prev_date else None
        insertPatch(patch)
        prev_date = patch['date_start']


def convert_float_to_int(value):
    return int(value) if value.is_integer() else value


def patch_key(version):
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', version)]


def special_case_for_set_five_because_people_who_manage_websites_hate_us(patch_id):
    return 5.5 if float(patch_id) in [11.15, 11.16, 11.17, 11.18, 11.19, 11.20, 11.21] else 5.0
