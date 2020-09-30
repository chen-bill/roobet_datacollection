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
while(True):
    print('---------Collecting---------')
    html = driver.page_source
    soup = BeautifulSoup(html, features="html5lib")
    crashDivs = soup.findAll('div', class_='jss108')

    newCrashList = []
    for div in crashDivs:
        num = div.span.text
        num = num.replace('x', '')
        newCrashList.append(float(num))
    newCrashList = list(reversed(newCrashList))

    crashList.append(newCrashList)
    print('new crash list', newCrashList)

    # print('crashList', crashList)

    # if len(crashList) != 0:
        # crashListIndex = -1
        # while True:
            # try:
                # print("crashListIndex", crashListIndex)
                # print("crashList[]", crashList[crashListIndex])
                # lastCrashIndex = newCrashList.index(crashList[crashListIndex])
                # print("lastCrashIndex", lastCrashIndex)

                # if (lastCrashIndex != len(newCrashList)):
                    # print("Adding: ", newCrashList[lastCrashIndex+1:])
                    # crashList.extend(newCrashList[lastCrashIndex+1:])
                # break
            # except:
                # crashListIndex = crashListIndex - 1

    # else:
        # crashList = newCrashList

    # print('Final crash list:', crashList)

    with open(CRASH_LIST_FILE, "wb") as crashListFile:
        pickle.dump(
            crashList,
            crashListFile,
            protocol=pickle.HIGHEST_PROTOCOL)

    sleep(60)

    # driver.close()
