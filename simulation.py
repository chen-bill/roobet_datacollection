from selenium import webdriver
import pickle
import bs4
import os
from time import sleep
from bs4 import BeautifulSoup

CRASH_LIST_FILE = "crash.pickle"

if os.path.isfile(CRASH_LIST_FILE):
    with open(CRASH_LIST_FILE, "rb") as f:
        crashList = pickle.load(f)
else:
    crashList = []

driver = webdriver.Chrome()
driver.get('https://roobet.com/crash')

prevCrash = 1.0
money = 20.0

#autoCashout is in multiplier form for simulation purposes
def makeBet(betAmount, autoCashout, crash):
    print('Making bet', betAmount, autoCashout, crash)
    if betAmount * autoCashout < crash:
        print('Win', betAmount * autoCashout)
        return betAmount * autoCashout
    else:
        print('Lose', betAmount)
        return -betAmount

def makeRealBet():
    driver.find_element_by_css_selector('.button .c_button .s_button').click()


# Wait to log in and change auto cashout
input("Change AutoCashout and bet amount. Press enter to continue...")

while(True):
    print('Holdings:', money)
    html = driver.page_source
    soup = BeautifulSoup(html, features="html5lib")
    crashDivs = soup.findAll('div', class_='jss108')

    if len(crashDivs) == 0:
        sleep(1)
        continue

    crashVal = float(crashDivs[0].span.text.replace('x', ''))

    if crashVal != prevCrash:
        #other bet conditions:
        if crashVal > 2.0:
            button = driver.find_element_by_css_selector('.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedSecondary.MuiButton-fullWidth')
            button.click()
            print('Placing bet...')
            # money += makeBet(1, 1.5, crashVal)
        #make bet button click

        prevCrash = float(crashVal)

    sleep(1)

    # driver.close()

