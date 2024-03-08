import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from get_games import getGame

from webdriver_selenium import loadProfilePage
from webdriver_selenium import staleElementLoop
from webdriver_selenium import clickExpand

from tft.misc import insertPlayer

class tftQuery():
    def __init__(self, numOfQueries=10):
        self.gameJSON = []
        self.numOfQueries = int(numOfQueries)
        self.path = None
        self.jsonPath = os.getcwd() + '/tft_selenium/data/names.json'
        self.playerFolder = os.getcwd() + '/tft_selenium/data/players/'

    def queryPlayer(self, url):
        browser = loadProfilePage(url)
        if not browser:
            print("Player Not Found")
            # call delete function
            # call save position function
            return False

        wait = WebDriverWait(browser, timeout=5)

        xpath = "/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[4]/div[2]/div[2]"
        container = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        gameList = container.find_elements(By.XPATH, './child::*')[1:]

        playerName = url[34:]
        region = url[31:33]

        playerID = insertPlayer({'player_name': playerName, 'region': region})

        for game in gameList:
            gameDate = staleElementLoop(game, ".PlayerMatchSummarySecondary", 3)
            # If unable to get gameDate, skip game
            if not gameDate:
                continue

            # If found game older than a month, end loop and query for player
            if "month" in gameDate.text:
                print("Found game older than month, ending query")
                break

            clickExpand(game)

            gameInfo = getGame(game, playerID)
            if not gameInfo:
                print("Game exists in database, skipping game")
                continue



tft = tftQuery()
url = "https://www.metatft.com/player/na/Drogo98-NA1"
tft.queryPlayer(url)