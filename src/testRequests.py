from requests import Requests



def testRequests():
    request = Requests()

    requests = {
        "TOP 10 GOLD" : request.getTop10Gold(),
        "PLAYER MOST CHAR CLASS" : request.getPlayerMostCharClass(),
        "BEST REWARD PER LVL" : request.getBestRewardPerLvl(),
        "NPC MOST GOLD" : request.getNpcMostGold(),
        "MOST COMMON ITEM TYPE LVL 5" : request.getMostCommonItemTypeLvl5(),
        "MONSTER HIGHEST REWARD" : request.getMonsterHighestReward()

    }
    i = 1
    for requestName, requestResult in requests.items():
        if requestResult is None:
            print(f"Warning: {requestName} returned None")
        else:
            request.db.displayFetchedData(requestResult)
            i+= 1
        

if __name__ == "__main__":
    testRequests();