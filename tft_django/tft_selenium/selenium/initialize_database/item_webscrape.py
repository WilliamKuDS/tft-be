from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from tft_selenium.selenium.webdriver_selenium import load_headless_browser

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")
django.setup()

from tft.misc import insertItem

RETRY_LIMIT = 3

def extract_item_details(item_container, url, item_type):
    item_dict = {}
    try:
        item_h2_elements = WebDriverWait(item_container, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h2')))

        item_set = float(item_h2_elements[0].text.split(' ')[1])
        item_set = round(item_set * 2) / 2
        item_dict['set_id'] = item_set

        item_name_unformatted = item_h2_elements[1].text.splitlines()[0]
        item_dict['display_name'] = item_name_unformatted
        item_name_formatted = ''.join(e for e in item_name_unformatted if e.isalnum())
        if item_type == 'component':
            item_dict['item_id'] = f"TFT_Item_{item_name_formatted}"
        else:
            item_dict['item_id'] = f"TFT{item_set}_Item_{item_name_formatted}"
        item_dict['name'] = item_name_formatted.lower()

        item_image_url = item_container.find_element(By.TAG_NAME, 'section').find_element(By.TAG_NAME, 'a').get_attribute('href')
        item_dict['icon'] = item_image_url

        try:
            if item_type == 'component':
                raise Exception(';(')
            item_recipe_element = item_container.find_element(By.CSS_SELECTOR, '[data-source="recipe"]')
            item_dict['recipe'] = item_recipe_element.text.splitlines()[1:]
        except Exception:
            item_dict['recipe'] = None

        item_info_elements = item_container.find_elements(By.TAG_NAME, 'section')[1].find_elements(By.XPATH, './child::*')
        item_info = clean_item_info(item_info_elements)
        item_dict.update(item_info)

        insertItem(item_dict)
    except Exception as e:
        print(f"Unexpected error extracting item details from {url}: {e} \n {item_dict}")
        return None

def get_item_info(item_url, item_type, retry_count=0):
    if retry_count > RETRY_LIMIT:
        print(f"Failed to process {item_url} after {RETRY_LIMIT} retries.")
        return None

    browser = load_headless_browser()
    try:
        browser.get(item_url)
        wait = WebDriverWait(browser, 3)

        try:
            if 'Guardian_Angel' in item_url or "Thief%27s_Gloves" in item_url:
                raise Exception(';(')
            tab_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.tabber.wds-tabber')))
            tabs = tab_container.find_elements(By.CSS_SELECTOR, '.wds-tabs__tab')

            for tab in tabs:
                browser.execute_script("arguments[0].click();", tab)
                current_tab = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.wds-tab__content.wds-is-current')))
                extract_item_details(current_tab, item_url, item_type)
        except Exception:
            main_content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mw-parser-output')))
            extract_item_details(main_content, item_url, item_type)

    except Exception as e:
        print(f"Error processing {item_url}: {e}. Retrying ({retry_count+1}/{RETRY_LIMIT})...")
        return get_item_info(item_url, retry_count + 1)
    finally:
        browser.quit()

def clean_item_info(item_info_elements):
    clean_item_info_dict = {}
    stat_list = ['Attack damage', 'Ability power', 'Attack speed', 'Health', 'Starting mana', 'Armor', 'Magic resist', 'Crit. chance']
    tag_list = ['RADIANT', 'EXCLUSIVE', 'UNIQUE', 'SUPPORT', "ELUSIVE", "ONLY FOR KAYLE", 'ARTIFACT']

    item_tag_list, item_stats_list = [], []
    for element in item_info_elements:
        text_lines = element.text.splitlines()

        if 'Passive' in text_lines:
            clean_item_info_dict['description'] = ' '.join(text_lines[1:])
        elif 'Recipe' in text_lines:
            clean_item_info_dict['recipe'] = text_lines[1:]
        elif any(stat in text_lines for stat in stat_list):
            item_stats_list.append(' '.join(text_lines))
        elif any(tag in text_lines for tag in tag_list):
            item_tag_list.append(text_lines[0])

    clean_item_info_dict['stats'] = item_stats_list
    clean_item_info_dict['tags'] = item_tag_list

    if 'description' not in clean_item_info_dict:
        clean_item_info_dict['description'] = None
    return clean_item_info_dict

def scrape_tft_items(tft_item_url, item_type):
    browser = load_headless_browser()
    wait = WebDriverWait(browser, 5)

    try:
        browser.get(tft_item_url)
        while True:
            item_urls = [
                element.get_attribute('href') for element in wait.until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'category-page__member-link'))
                )
                if 'Item_' not in element.get_attribute('href') and 'Old_TFT_item_' not in element.get_attribute('href') and 'TFT_' not in element.get_attribute('href')
            ]

            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_url = {executor.submit(get_item_info, url, item_type): url for url in item_urls}
                for future in tqdm(as_completed(future_to_url), total=len(future_to_url), desc="Scraping items"):
                    future.result()

            try:
                next_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'category-page__pagination-next.wds-button.wds-is-secondary')))
                next_button_url = next_button.get_attribute('href')
                browser.get(next_button_url)
            except Exception:
                break
    finally:
        browser.quit()

# MAIN
tft_components_url = "https://leagueoflegends.fandom.com/wiki/Category:TFT_component"
scrape_tft_items(tft_components_url, 'component')
tft_item_url = 'https://leagueoflegends.fandom.com/wiki/Category:TFT_items'
scrape_tft_items(tft_item_url, 'item')
