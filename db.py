from replit import db
from pokemoncard import getCard

packWait = 600  # Seconds


def getTimeLeft(id, time):  # in seconds
    try:
        return packWait + db[
            str(id) + "t"] - time  # Should not be setting the db to anything
    except:
        return 0


def getPacks(id):
    try:
        return db[str(id) + "p"]
    except:
        db[str(id) + "p"] = 0
        return 0


def freePacks(id, time):  # Deprecated
    try:
        timePassed = time - db[str(id) + "t"]  # Time passed
        extraPacks = timePassed // packWait  # Total time passed divided by time necesasry to pass is how many new packs you get

        db[str(id) + "p"] += int(extraPacks)  # add the new packs on

        if db[str(id) + "p"] > 10:
            db[str(id) +
               "p"] = 10  # If you overload on free packs, reset to 10
            db[str(id) + "t"] = time  # Also, set new timer start from here
        elif db[str(id) + "p"] > 0:
            # You have not overloaded, you are fine
            db[str(id) + "t"] = int(
                time + (timePassed % packWait) - packWait
            )  # Set new timer to a few minutes ago when the newest pack stopped counting

            # Check out this last line of code
            # Ensure that running 'c.card' multiple times does not decrease time for next card

        # If you didnt get any packs, nothing changes

    except:
        db[str(id) + "p"] = 10
        db[str(id) + "t"] = time


def freePacks2(id, time):
    try:
        timePassed = time - db[str(id) + "t"]  # Time passed
        extraPacks = int(
            timePassed // packWait
        )  # Total time passed divided by time necesasry to pass is how many new packs you get

        if extraPacks != 0:
            db[str(id) + "p"] += int(extraPacks)  # add the new packs on
            if db[str(id) + "p"] >= 10:
                db[str(id) + "p"] = 10
                db[str(id) + "t"] = time
            else:
                db[str(id) +
                   "t"] = db[str(id) +
                             "t"] = int(time + (timePassed % packWait) -
                                        packWait)

    except:
        db[str(id) + "p"] = 10
        db[str(id) + "t"] = time


def updatePacks(id, num):
    try:
        db[str(id) + "p"] = int(db[str(id) + "p"] + num)
        return True
    except:
        db[str(id) + "p"] = 0
        return False
    pass


#Collection DB


def getCollection(id):
    try:
        return db[str(id) + "c"]
    except:
        return {}


def addToCollection(id, card, quantity=1):
    print("adding to collection for " + str(id))

    try:
        col = db[str(id) + "c"]

        try:
            # db[str(id)+"c"][card.name]=db[str(id)+"c"][card.name]+int(1)
            if quantity + col[card.name] < 0: return False
            col[card.name] = col[card.name] + int(quantity)

        except:
            # db[str(id)+"c"][card.name]=int(1)
            if quantity < 0: return False
            col[card.name] = int(quantity)

    except:
        col = {}
        if quantity < 0: return False
        col[card.name] = int(quantity)
    finally:
        col = removeZerosFromCollection(col)
        db[str(id) + "c"] = col
        return True


def removeZerosFromCollection(collection):
    withoutZeros = {}
    for card in collection:
        if collection[card] != 0:
            withoutZeros[card] = collection[card]
    return withoutZeros


def addDictToCollection(id, cardDict={}, cardNameDict={}):

    for card in cardDict:
        addToCollection(id, card=card, quantity=int(cardDict[card]))
    for cardName in cardNameDict:
        addToCollection(id, getCard(card), quantity=int(cardNameDict[card]))


#Trading DB


def initTradeList():
    try:
        list = db["trade"]
    except:
        db["trade"] = []


def getTradeList():
    initTradeList()
    return db["trade"]


def addTradeList(pair):
    initTradeList()
    tradeList = db["trade"]
    tradeList.append(pair)
    db["trade"] = tradeList


def removeTradeList(channelID, msgID):
    initTradeList()
    print(db["trade"])

    tradeList = db["trade"]
    for pair in tradeList:
        print(pair)
        if channelID == pair[0][0] or msgID == pair[0][1]:
            tradeList.remove(pair)
            return pair
        elif channelID == pair[1][0] and msgID == pair[1][1]:
            tradeList.remove(pair)
            return pair
    db["trade"] = tradeList
