from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import winsound

ser = Service("C:\webdrivers\chromedriver.exe")  # Replace with Chrome driver location

LOGIN_LINK = "https://online.nzta.govt.nz/licence-test/identification"

# Fill in information
LICENSE_NUMBER = "LICENSE NUMBER"
LICENSE_VERSION = "LICENSE VERSION"
SURNAME = "SURNAME"
BIRTHDATE = "DD-MM-YYYY"  # DD-MM-YYYY


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

browser = webdriver.Chrome(options=options, service=ser)


def isAvailable():
    WebDriverWait(browser, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.ui-datepicker-next"))
    ).click()
    time.sleep(5)
    if len(browser.find_elements(By.CSS_SELECTOR, "td.ui-datepicker-current-day")) > 0:
        return True

    WebDriverWait(browser, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.ui-datepicker-prev"))
    ).click()
    time.sleep(5)

    return (
        len(browser.find_elements(By.CSS_SELECTOR, "td.ui-datepicker-current-day")) > 0
    )


def type(element, msg):
    for char in msg:
        element.send_keys(char)
        time.sleep(random.uniform(0.02, 0.2))


def login():
    print(f"{datetime.now().strftime('%I:%M %p')} >> Logging in!")
    browser.get(LOGIN_LINK)
    license = WebDriverWait(browser, 120).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[formcontrolname="LicenceNumber"]')
        )
    )
    version = WebDriverWait(browser, 120).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[formcontrolname="LicenceVersion"]')
        )
    )
    last = WebDriverWait(browser, 120).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[formcontrolname="LastName"]')
        )
    )
    birth = WebDriverWait(browser, 120).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[formcontrolname="DateOfBirth"]')
        )
    )
    continue_btn = WebDriverWait(browser, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#btnContinue"))
    )

    type(license, LICENSE_NUMBER)
    time.sleep(random.uniform(0.2, 0.6))
    type(version, LICENSE_VERSION)
    time.sleep(random.uniform(0.2, 0.6))
    type(last, SURNAME)
    time.sleep(random.uniform(0.2, 0.6))
    type(birth, BIRTHDATE)
    time.sleep(random.uniform(0.2, 0.6))
    continue_btn.click()

    time.sleep(random.uniform(2, 5))
    reschedule_btn = WebDriverWait(browser, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#btnContinue"))
    )
    reschedule_btn.click()

    # Get to northshore
    WebDriverWait(browser, 120).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Auckland"))
    ).click()
    time.sleep(random.uniform(0.2, 0.6))
    WebDriverWait(browser, 120).until(
        EC.presence_of_element_located((By.LINK_TEXT, "North Auckland"))
    ).click()
    time.sleep(random.uniform(0.2, 0.6))
    WebDriverWait(browser, 120).until(
        EC.presence_of_element_located((By.LINK_TEXT, "VTNZ North Shore"))
    ).click()


def alert():
    while True:
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        time.sleep(0.5)


def main():
    while True:
        try:
            login()

            while True:
                result = isAvailable()
                print(f"{datetime.now().strftime('%I:%M %p')} >> {result}")
                if result:
                    alert()

                time.sleep(60)

        except:
            pass


main()
