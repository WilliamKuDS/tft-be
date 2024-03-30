import os
from datetime import date
import re

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_selenium import loadProfilePage, staleElementLoop, is_element_visible
from get_games import getGame
from tft.misc import insertPlayer
from tft.models import game as game_model


class tftQuery():
    def __init__(self, numOfQueries=10):
        self.gameJSON = []
        self.numOfQueries = int(numOfQueries)
        self.path = None
        self.jsonPath = os.getcwd() + '/tft_selenium/data/names.json'
        self.playerFolder = os.getcwd() + '/tft_selenium/data/players/'
        self.errorCounter = 0

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
        icon = browser.find_element(By.CLASS_NAME, 'PlayerProfileIconImage').get_attribute('src')
        playerRank = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[4]/div[1]/div/div[1]/div[3]').text.split('\n')
        playerLP = re.sub('\D', '', playerRank[1])
        playerRank = playerRank[0]

        playerID = insertPlayer({'player_name': playerName, 'region': region, "last_updated": date.today(), 'icon': icon, 'player_rank': playerRank, 'player_lp': playerLP})

        for game in gameList:
            try:
                gameID = game.get_attribute("id")
                dateElement = '#' + gameID + '> div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)'
                gameDate = staleElementLoop(game, dateElement, 3)
                # If unable to get gameDate, skip game
                if not gameDate:
                    print("Unable to get game date, skipping game")
                    self.errorCounter += 1
                    continue

                # If found game older than a month, end loop and query for player
                if "month" in gameDate.text:
                    print("Found game older than month, ending query")
                    break

                gameObject = game_model.safe_get_player_game_id(player_id=playerID, game_id=gameID)
                if gameObject:
                    print("Game exists in database, skipping game")
                    continue

                gameInfo = getGame(game, playerID)
                if not gameInfo:
                    print("Error in inserting Game, skipping game")
                    self.errorCounter += 1
                    continue


                if not is_element_visible(browser, "/html/body/div[1]/div/div[2]/div[3]"):
                    browser.execute_script("window.scrollBy(0, 3000)")
                    browser.execute_script("window.scrollBy(0, -3000)")
            except StaleElementReferenceException:
                print("Unable to get game date, skipping game")
                continue
        print("Finished querying {}".format(playerName))
        browser.close()

# tft = tftQuery()
# tft.queryPlayer('https://www.metatft.com/player/na/Drogo98-NA1')