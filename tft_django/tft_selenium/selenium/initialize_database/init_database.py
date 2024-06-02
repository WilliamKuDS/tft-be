from set_patch_webscrape import webscrape_set_and_patch_and_save_set_to_db, webscrape_patch_urls, save_entire_patch_list_to_db
from tft_selenium.selenium.webdriver_selenium import loadPage
set_url = 'https://leagueoflegends.fandom.com/wiki/Template:TFT_release_history'

browser = loadPage(set_url)
set_patch_dict = webscrape_set_and_patch_and_save_set_to_db(browser)
print('Finished adding sets to database')

full_patch_list = []
for tft_set in set_patch_dict:
    set_patch_list = webscrape_patch_urls(browser, tft_set['patch_url_list'], tft_set['set_id'])
    full_patch_list = [*full_patch_list, *set_patch_list]
save_entire_patch_list_to_db(full_patch_list)
print('Finished adding patches to database.')

