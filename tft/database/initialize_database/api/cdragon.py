import requests
import traceback

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tft_django.settings")
django.setup()

from cdragon_functions import read_trait_and_add_to_database, read_champion_and_add_to_database, read_item_or_augment_and_add_to_database
from tft.models import patch as patchModel

patch_list = patchModel.objects.all()
for patch in patch_list:
    patch_id = patch.patch_id

    # Skip patch 9.13, as it was the first patch for tft and unable to find tft data in cdragon
    # Will try in future update to see if 9.13 TFT is stored somewhere
    if patch_id == '9.13':
        continue

    # latest patch is labeled 'latest' not by patch number
    if patch.date_end == None:
        url_patch_id = 'latest'
    # These patches don't exist in cdragon on the base level. Will use next patch data to fill in for now.
    elif patch_id == '13.2':
        url_patch_id = '13.3'
    elif patch_id == '10.17':
        url_patch_id = '10.18'
    else:
        url_patch_id = patch_id

    set_id, midPatch = int(patch.set_id.set_id), not patch.set_id.set_id.is_integer()

    try:
        tft_patch_data_url = "https://raw.communitydragon.org/{}/cdragon/tft/en_us.json".format(url_patch_id)
        tft_patch_data_response = requests.get(tft_patch_data_url)
        tft_patch_data_json = tft_patch_data_response.json()

        # client_metadata_url = "https://raw.communitydragon.org/{}/system.yaml".format(patch_id)
        # client_metadata_response = requests.get(client_metadata_url)
        # client_metadata = yaml.safe_load(client_metadata_response.text)
        # tft_patch_data = client_metadata['build']['branch'].split('/')[1]

        if not midPatch or set_id == 3:
            mutator_ids = ['TFTSet' + str(set_id), 'TFT_Set' + str(set_id)]
        else:
            mutator_ids = ['TFTSet' + str(set_id) + '_Stage2', 'TFT_Set' + str(set_id) + '_Stage2', 'TFTSet' + str(set_id) + '_Act2']

        if 'setData' in tft_patch_data_json:
            champions_and_traits_data = next((item for item in tft_patch_data_json['setData'] if item.get('mutator') in mutator_ids), None)
        else:
            champions_and_traits_data = tft_patch_data_json['sets'][str(set_id)]

        champion_data = champions_and_traits_data['champions']
        traits_data = champions_and_traits_data['traits']
        [read_trait_and_add_to_database(trait, patch_id) for trait in traits_data]
        [read_champion_and_add_to_database(champion, patch_id) for champion in champion_data]

        augments_and_items_data = tft_patch_data_json['items']
        [read_item_or_augment_and_add_to_database(data, patch_id) for data in augments_and_items_data]

    except Exception as e:
        print('{} failed. Error: {}'.format(url_patch_id, e))
        print(traceback.format_exc())
