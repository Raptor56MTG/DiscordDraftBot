from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from decouple import config


def take_screenshot():
    """This takes a screenshot of the sheet after the draft is over.
    This will then be posted to the server for future reference."""

    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = config('GOOGLE_CHROME_BIN')

    PATH = config('CHROMEDRIVER_PATH')
    driver = webdriver.Chrome(options=options, executable_path=PATH)

    # set size of image for screenshot
    driver.set_window_size(1325, 1200)
    driver.maximize_window()

    # let the driver wait a bit before requesting
    driver.implicitly_wait(5)
    driver.get(config('DOCS_LINK'))

    # wait for page to load then take the screenshot and quit
    driver.implicitly_wait(30)
    driver.get_screenshot_as_file("completed_draft.png")
    driver.close()
    driver.quit()
