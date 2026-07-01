
# this file uses local storage folder for browser data
# login to the account before executing the actual script
from os import path, mkdir, remove, chmod
import sys
from urllib import request
import json
from zipfile import ZipFile
from time import sleep
from shutil import rmtree


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

home_directory = path.expanduser("~")
local_bin_directory = home_directory + '/bin'



def loginWindow():
    print(local_bin_directory)
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={local_bin_directory}/chrome-data")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    # chrome_options.add_experimental_option('excludeSwitches',
    # ["enable-automation"])

    service = Service()
    driver = None

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except SessionNotCreatedException:
        print("Update your chrome to latest version, then run again. Also, try to Reset the Setup.")
        sys.exit()
    driver.get("https://linkedin.com/")

    # second tab
    driver.execute_script("window.open('about:blank', 'secondtab');")
    driver.switch_to.window("secondtab")

    # In the second tab
    driver.get('https://naukri.com/')
    sleep(120)
    driver.close()
    driver.quit()


def reset():
    try:
        rmtree(local_bin_directory + "/chromedriver")
    except:
        print("reset failed, manually delete files in " + local_bin_directory + "/chromedriver")
