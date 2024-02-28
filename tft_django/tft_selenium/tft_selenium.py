from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time
import re
import argparse


class tftQuery():
    def __init__(self, numofGames=10):
        self.gameJSON = []
        self.numOfGames = int(numofGames)
        self.path = None
        self.playerList = set()
        self.jsonPath = os.getcwd() + '/tft_selenium/data/names.json'
        self.playerFolder = os.getcwd() + '/tft_selenium/data/players/'

    ''' getInfo function
    Input:
    Initialized with url and max number of games to search

    Output:
    Creates two 


    '''

    def getInfo(self, url):
        browser = self.loadPage(url)

        self.path = self.playerFolder + url[34:] + '.json'

        gameID_duplicates = self.getDuplicates('GameID', self.path)

        if not os.path.isfile(self.path):
            self.formatData({'URL': url}, self.path)

        gameInfo = browser.find_elements(By.CLASS_NAME, 'PlayerGame')
        count = 0
        for game in gameInfo:
            if count == self.numOfGames:
                break

            gameInfo = {}

            # Get GameID
            gameID = game.get_attribute('id')
            if gameID in gameID_duplicates:
                continue

            gameInfo['PlayerGameID'] = url[34:] + '-' + gameID
            gameInfo['PlayerName'] = url[34:]
            gameInfo['GameID'] = gameID

            gameInfo = self.getPlayerSummary(game, gameInfo)
            gameInfo = self.getPlayerTraits(game, gameInfo)
            gameInfo = self.getPlayerUnits(game, gameInfo)
            # Add gameInfo to JSON file
            self.formatData(gameInfo, self.path)

            self.getOtherPlayers(game)

            count += 1

        self.saveOtherPlayers()
        browser.quit()

    def getDuplicates(self, checkValue, path):
        try:
            duplicates = set()
            with open(path, 'r') as f:
                for line in f.readlines():
                    duplicates.add(json.loads(line).get(checkValue))
            return duplicates
        except FileNotFoundError:
            return set()

    def formatData(self, gameStats, path):
        with open(path, "a+", encoding='utf-8') as outfile:
            temp = json.dumps(gameStats)
            outfile.write(temp + '\n')

    def getNameLoop(self, item):
        tempList = []
        items = item[0].find_elements(By.CLASS_NAME, "display-contents")
        for i in items:
            name = i.find_element(By.TAG_NAME, 'img').get_attribute('alt')
            tempList.append(name)
        return tempList

    def loadPage(self, url):
        browser = webdriver.Firefox()
        browser.get(url)

        wait = WebDriverWait(browser, timeout=2)

        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'PlayerGameMatch')))
        except:
            browser.quit()
            raise Exception("No Player Found")

        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "PlayerGameMatch")))

        # elem = browser.find_element(By.TAG_NAME, "html")
        # elem.send_keys(Keys.END)
        SCROLL_PAUSE_TIME = 0.25
        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        return browser

    def getPlayerSummary(self, game, gameInfo):
        gameType = game.find_elements(By.CLASS_NAME, 'PlayerMatchSummaryQueue')
        gameInfo['Queue'] = gameType[0].text

        # Get Match Placement
        placement = game.find_elements(By.CLASS_NAME, "PlayerMatchSummaryPlacement")
        gameInfo['Placement'] = int(placement[0].text)

        # Get Match Level
        level = game.find_elements(By.CLASS_NAME, "PlayerLevel")
        gameInfo['Level'] = int(level[0].text)

        # Get Match Summary [Length + Round]
        summary = game.find_elements(By.CLASS_NAME, "PlayerMatchSummarySecondary")
        summaryList = summary[1].text.replace(" • ", " ").split(" ")
        gameInfo['Length'] = summaryList[0]
        gameInfo['Round'] = summaryList[1]

        # Get Match Augments
        augments = game.find_elements(By.CLASS_NAME, "PlayerMatchAugments")
        gameInfo['Augments'] = self.getNameLoop(augments)

        return gameInfo

    def getPlayerTraits(self, game, gameInfo):
        traits = game.find_elements(By.CLASS_NAME, "PlayerMatchTraits")

        # Checks if match has traits, if not return empty list
        if len(traits[0].text) == 0:
            gameInfo['Traits'] = []
            gameInfo['Headliner'] = 'None'
            return gameInfo

        # Get Match Headliner
        headliner = game.find_elements(By.CLASS_NAME, "OptionName.HeadlinerTraitText")
        if len(headliner) > 0:
            gameInfo['Headliner'] = re.sub("[^a-zA-Z] ", "", headliner[0].text).strip(',')
        else:
            gameInfo['Headliner'] = 'None'

        # Get Match Traits
        traitList = traits[0].text.split(',\n')
        traitDict = {}
        for trait in traitList:
            temp = trait.split(' ')
            traitDict[temp[1]] = int(temp[0])
        gameInfo['Traits'] = [traitDict]

        return gameInfo

    def getPlayerUnits(self, game, gameInfo):
        # Get Match Units
        units = (game.find_elements(By.CLASS_NAME, 'Unit_Wrapper'))
        unitList = []
        # Each Unit has a subset of items
        for unit in units:
            unitInfo = {}

            # Get unit's name
            images = unit.find_elements(By.CLASS_NAME, 'display-contents')
            name = images[0].find_element(By.TAG_NAME, 'img').get_attribute('alt')
            unitInfo['Name'] = name
            itemsContainers = unit.find_elements(By.CLASS_NAME, 'ItemsContainer')

            # Get unit's tier level [1,2,3]
            tiers = unit.find_elements(By.CLASS_NAME, 'Stars_img')
            if len(tiers) > 0:
                tier = tiers[0].get_attribute('alt')
                unitInfo['Tier'] = int(tier[5:])
            else:
                unitInfo['Tier'] = 1

            # Get each unit's items
            items = self.getNameLoop(itemsContainers)
            unitInfo['Items'] = items

            # Append each unit to UnitList
            unitList.append(unitInfo)

        # Append UnitList to gameInfo Dictionary
        gameInfo['Units'] = unitList

        return gameInfo

    def getOtherPlayers(self, game):
        # Get Other data in Match
        # Click drop down button for each game
        wait = WebDriverWait(game, timeout=2)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "PlayerGameMatch")))
        game.find_elements(By.CLASS_NAME, 'Expand')[0].click()
        players = game.find_elements(By.CLASS_NAME, 'PlayerMatchNameLink')

        player_duplicates = self.getDuplicates('URL', self.jsonPath)

        for player in players:
            href_player = player.get_attribute('href')
            if href_player in player_duplicates:
                continue
            self.playerList.add(href_player)

    def saveOtherPlayers(self):
        for player in self.playerList:
            value = {"URL": player}
            self.formatData(value, self.jsonPath)

    def getSubPlayers(self, numOfPlayers):
        count = 0
        with open(self.jsonPath, 'r') as playerList:
            for player in playerList.readlines():
                if count == int(numOfPlayers):
                    break
                url = json.loads(player).get('URL')
                path = self.playerFolder + url[34:] + '.json'
                if os.path.isfile(path):
                    continue
                self.getInfo(url)
                count += 1

    def updatePlayers(self):
        for playerJson in os.listdir(self.playerFolder):
            file = os.path.join(self.playerFolder, playerJson)
            with open(file, 'r') as outfile:
                url = json.loads(outfile.readlines()[0])['URL']
                self.getInfo(url)


def getURL(name, region, tag):
    return 'https://www.metatft.com/player/' + region + '/' + name + '-' + tag


def parseQuery():
    parser = argparse.ArgumentParser(description='Enter Query Type')
    subparsers = parser.add_subparsers(dest='query', help='sub-command help')
    # parser.add_argument('-m', '--mode', action='store', help='Specify mode 1 (Query Player) or 2 (Query Subplayers)')

    parserMode_1 = subparsers.add_parser('1', help='Query Specific Player')
    parserMode_1.add_argument('-n', '--name', type=str, required=True, help='Player Name')
    parserMode_1.add_argument('-t', '--tag', type=str, required=True, help='Player Tag')
    parserMode_1.add_argument('-r', '--region', type=str, required=True, help='Player Region')
    parserMode_1.add_argument('-l', '--length', type=int, help='Amount of Matches to Query')

    parserMode_2 = subparsers.add_parser('2', help='Query Subplayers')
    parserMode_2.add_argument('-a', '--player_amount', type=int, required=True, help='Amount of Players to Query')
    parserMode_2.add_argument('-l', '--length', type=int, required=True, help='Amount to Matches to Query')

    parserMode_3 = subparsers.add_parser('3', help='Update Players')

    return parser.parse_args()


if __name__ == '__main__':
    args = parseQuery()
    if args.query == '1':
        url = getURL(args.name, args.region.lower(), args.tag)
        player = tftQuery(args.length)
        player.getInfo(url)
    elif args.query == '2':
        player = tftQuery(args.length)
        player.getSubPlayers(args.player_amount)
    elif args.query == '3':
        player = tftQuery()
        player.updatePlayers()
