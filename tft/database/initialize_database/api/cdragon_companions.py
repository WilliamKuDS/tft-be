import requests
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")
django.setup()

from tft.utils.insert_functions import insertCompanion


tft_companion_url = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/companions.json'
tft_companion_data_response = requests.get(tft_companion_url)
tft_companion_data_json = tft_companion_data_response.json()

for tft_companion in tft_companion_data_json:
    insertCompanion(tft_companion)
