import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initBrowser():
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    options.add_argument("start-maximized")
    browser = webdriver.Firefox(options=options)
    # browser.maximize_window()
    #options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    #options.add_argument('--start-maximized')
    #browser = webdriver.Chrome(options=options)
    return browser

def load_headless_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-images")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-javascript")
    options.add_argument("start-maximized")
    options.add_argument("window-size=1920,1080")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

def scroll_down(browser):
    """A method for scrolling the page."""
    print("Scrolling Page")
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

def staleElementLoopForClickExpand(browser, element, attempts):
    wait = WebDriverWait(browser, timeout=2)
    for i in range(attempts):
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, element))).click()
            break
        except Exception as e:
            print("Error {}, Trying Again. Attempt: {}. Element: {}".format(e, i, element))

def staleElementLoopByClass(browser, element, attempts):
    wait = WebDriverWait(browser, timeout=2)
    for i in range(attempts):
        try:
            data = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, element)))
            return data
        except Exception as e:
            print("Error {}, Trying Again. Attempt: {}. Element: {}".format(e, i, element))
    return False

def staleAllElementsLoopByClass(browser, element, attempts):
    wait = WebDriverWait(browser, timeout=2)
    for i in range(attempts):
        try:
            data = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, element)))
            return data
        except Exception as e:
            print("Error {}, trying Again. Attempt: {}. Element: {}".format(e, i, element))
    return False

def staleElementLoop(browser, element, attempts):
    wait = WebDriverWait(browser, timeout=2)
    for i in range(attempts):
        try:
            data = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, element)))
            return data
        except Exception as e:
            print("Error {}, trying Again. Attempt: {}. Element: {}".format(e, i, element))
    return False

def staleElementLoopByXPath(browser, element, attempts):
    wait = WebDriverWait(browser, timeout=2)
    for i in range(attempts):
        try:
            data = wait.until(EC.visibility_of_element_located((By.XPATH, element)))
            return data
        except Exception as e:
            print("Error {}, trying Again. Attempt: {}. Element: {}".format(e, i, element))
    return False

def is_element_visible(browser, xpath):
    wait = WebDriverWait(browser, 2)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return True
    except Exception:
        return False

def loadProfilePage(url):
    print('Initializing browser')
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
    #scroll_down(browser)

    return browser

def loadPage(url):
    browser = initBrowser()
    browser.get(url)

    #scroll_down(browser)

    return browser

def quickLoadPage(url):
    browser = initBrowser()
    browser.get(url)
    return browser




