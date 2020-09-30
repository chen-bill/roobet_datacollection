import pickle
import os
import csv

CRASH_LIST_FILE = "crash.pickle"

if os.path.isfile(CRASH_LIST_FILE):
    with open(CRASH_LIST_FILE, "rb") as f:
        crashLists = pickle.load(f)
else:
    raise "Crash lists empty"

print(len(crashLists))

mainCrashList = crashLists[0]

for crashList in crashLists[1:]:
    # print('--------')
    # print('mainCrashList', mainCrashList)
    # print('crashList', crashList)

    mainCrashIndex = -1
    print('-------')
    while True:
        try:
            lastCrashValue = mainCrashList[mainCrashIndex]

            if len(crashList) == 0:
                break
            # print('lastCrashValue', lastCrashValue)

            lastCrashIndex = len(crashList) - crashList[::-1].index(lastCrashValue) - 1
            # print('lastCrashIndex', lastCrashIndex)

            if lastCrashIndex != len(crashList):
                toAdd = crashList[lastCrashIndex + 1:]
                # If crash index doens't work up to 3 times, assume disconnected data and just add
                if mainCrashIndex <= -3:
                    print('Adding', crashList)
                    mainCrashList.extend(crashList)
                    break
                elif mainCrashIndex != -1:
                    # print('mainCrashIndex', mainCrashIndex)
                    # print('deleting elements', mainCrashList[mainCrashIndex+1:])
                    del mainCrashList[mainCrashIndex+1:]
                    print('Adding', toAdd)
                    mainCrashList.extend(toAdd)
                else:
                    print('Adding', toAdd)
                    mainCrashList.extend(toAdd)
                break
            else:
                # print('Nothing new to add.')
                break
        except Exception as e:
            print('error here', e)
            mainCrashIndex = mainCrashIndex - 1

print('Done: ', mainCrashList)

with open('crashData.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for crash in mainCrashList:
        myfile.write(str(crash))
        myfile.write('\n')
        # wr.writerows(str(crash))

#---------simulation starts here

#every round
betAmounts = [1, 2, 5, 10, 20]
pullOutValues = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0]

# for betAmount in betAmounts:
    # for fullOutFactor in pullOutValues:
        # money = 50
        # print('-------')
        # print('bet', betAmount)
        # print('fullOutFactor', fullOutFactor)

        # for crash in mainCrashList:
            # money = money - betAmount
            # if money <= 0:
                # print('Dirt poor')
                # break
            # if crash > fullOutFactor:
                # money += betAmount * fullOutFactor
                # # print('money', money)
        # if money > 50:
            # print("THIS ONE", money)

def bet(betAmount, fullOutFactor, crash):
    if crash > fullOutFactor:
        # print('Win', betAmount * fullOutFactor)
        return betAmount * fullOutFactor - betAmount
    else:
        # print('Lose', -betAmount)
        return -betAmount

#  bet after red
money = 200
BET_SIZE = 0.01
BET_INCREASE_FACTOR = 2.03
AUTO_CASHOUT_FACTOR = 1.6
betSize = BET_SIZE

for ind, crash in enumerate(mainCrashList):
    print('-------')
    print('money', money)
    print('crash', crash)
    # print('prevCrash', mainCrashList[ind-1])
    # if mainCrashList[ind-1]:

    print('bet size', betSize)
    result = bet(betSize, AUTO_CASHOUT_FACTOR, crash)
    money += result
    if result < 0:
        betSize = betSize * BET_INCREASE_FACTOR
    else:
        betSize = BET_SIZE
    # print(money)

    if money <= 0:
        print('Dirt poor')
        break

#every other round
