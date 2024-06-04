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

def webscrape_set_and_patch_and_save_set_to_db(browser):
    wait = WebDriverWait(browser, timeout=5)

    expand_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mw-parser-output')))
    expand_box.find_element(By.TAG_NAME, 'a').click()

    container = browser.find_element(By.CSS_SELECTOR, "table.navbox.hlist")
    set_table = container.find_elements(By.XPATH, './tbody/child::*')
    final_set_patch_list = []

    for curr_set in set_table:
        set_patch_dict = {}
        set_text = curr_set.text.splitlines()[0]

        if 'Upcoming' in set_text:
            continue

        set_info = set_text.split(':', 1)
        set_id = float(set_info[0].strip(' Set '))
        set_patch_dict['set_id'] = set_id
        set_name = set_info[1].strip(' ')
        set_patch_dict['set_name'] = set_name
        insertSet(set_patch_dict)

        patch_list = curr_set.find_elements(By.TAG_NAME, 'li')
        patch_url_list = []

        for curr_patch in patch_list:
            patch_url = curr_patch.find_element(By.TAG_NAME, 'a').get_attribute('href')
            patch_url_list.append(patch_url)

        set_patch_dict['patch_url_list'] = patch_url_list
        final_set_patch_list.append(set_patch_dict)

    return final_set_patch_list

def webscrape_patch_urls(browser, patch_url_list, set_id):
    full_patch_list_for_set = []
    for patch_url in patch_url_list:
        patch_dict = {}
        browser.get(patch_url)
        wait = WebDriverWait(browser, timeout=5)

        patch_dict['set_id'] = set_id

        patch_info_container = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'aside')))

        patch_id = patch_info_container.find_element(By.TAG_NAME, 'h2').text.split(' ')[0].strip('V')
        patch_dict['patch_id'] = patch_id

        patch_info = patch_info_container.find_elements(By.TAG_NAME, 'section')

        patch_date_unformatted = patch_info[0].text.splitlines()[1]
        match = re.match(r'(\w+)\s(\d+)[a-z]{2},\s(\d{4})', patch_date_unformatted)
        if not match:
            raise ValueError("Date string format is incorrect")
        month, day, year = match.groups()
        # Construct the date string in a format that can be parsed by strptime
        formatted_date_string = f"{month} {day}, {year}"
        # Define the format and parse the date
        date_format = "%B %d, %Y"
        patch_date = datetime.strptime(formatted_date_string, date_format).date()
        patch_dict['date_start'] = patch_date

        patch_highlights = patch_info[1].text.splitlines()[1:]
        patch_dict['highlights'] = patch_highlights

        riot_patch_notes_url = patch_info[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
        patch_dict['patch_url'] = riot_patch_notes_url

        full_patch_list_for_set.append(patch_dict)

    return full_patch_list_for_set

def save_entire_patch_list_to_db(patch_list):
    def patch_key(version):
        parts = re.split(r'(\d+)', version)
        parts = [int(part) if part.isdigit() else part for part in parts]
        return parts

    # Sorting the list of dictionaries
    sorted_patch_list = sorted(patch_list, key=lambda x: patch_key(x['patch_id']), reverse=True)
    prev_date = None
    for patch in sorted_patch_list:
        if prev_date is None:
            patch['date_end'] = None
        else:
            patch['date_end'] = prev_date - timedelta(days=1)
        insertPatch(patch)
        prev_date = patch['date_start']







