from tft import misc
import os
import json
def saveAllPlayersInFolder():
    path = os.getcwd() + '/tft_selenium/data/players/'
    for filename in os.listdir(path):
        print('Saving {}'.format(filename))
        with open(path + filename, 'r') as data:
            for jsonLine in data.readlines()[1:]:
                misc.saveJSONToDatabase(json.loads(jsonLine))