import time

from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initBrowser():
    print('Initializing browser')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--start-maximized')
    browser = webdriver.Chrome(options=options)
    return browser

def scroll_down(browser):
    """A method for scrolling the page."""
    print("Scrolling Old_page")
    # Get scroll height.
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom.
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(1)
        # Calculate new scroll height and compare with last scroll height.
        new_height = browser.execute_script("return document.body.scrollHeight")
        # Checks if reached bottom of page
        if new_height == last_height:
            print("Finished Scrolling")
            break
        last_height = new_height

def clickExpand(browser):
    #css_element = '#' + playerName + ' > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2)'
    button = staleElementLoopByClass(browser, 'Expand', 5)
    button.click()

def staleElementLoopByClass(browser, element, attempts):
    wait = WebDriverWait(browser, timeout=5)
    for i in range(attempts):
        try:
            data = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, element)))
            return data
        except Exception as e:
            print("Error {}, Trying Again. Attempt: {}. Element: {}".format(e, i, element))
    return False

def staleAllElementsLoopByClass(browser, element, attempts):
    wait = WebDriverWait(browser, timeout=5)
    for i in range(attempts):
        try:
            data = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, element)))
            return data
        except Exception as e:
            print("Error {}, Trying Again. Attempt: {}".format(e, i))
    return False

def staleElementLoop(browser, element, attempts):
    wait = WebDriverWait(browser, timeout=5)
    for i in range(attempts):
        try:
            data = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, element)))
            return data
        except(StaleElementReferenceException):
            print("Data Stale, Trying Again. Attempt: {}".format(i))
    return False

def loadProfilePage(url):
    browser = initBrowser()
    browser.get(url)
    wait = WebDriverWait(browser, timeout=5)

    print('Checking if player exists')
    # Check if player exists, if not delete url from names.json
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.PlayerProfilePage')))
    except:
        return False

    print('Player found, starting query')
    scroll_down(browser)

    return browser

def loadPage(url):
    browser = initBrowser()
    browser.get(url)

    scroll_down(browser)

    return browser




