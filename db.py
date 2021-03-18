from replit import db



packWait = 600 # Seconds

def getTimeLeft(id, time): # in seconds
  try:
    return packWait + db[str(id)+"t"] - time # Should not be setting the db to anything
  except:
    return 0

def getPacks(id):
  try:
    return db[str(id)+"p"]
  except:
    db[str(id)+"p"] = 0
    return 0

def freePacks(id, time): # Deprecated
  try:
    timePassed = time-db[str(id)+"t"] # Time passed
    extraPacks = timePassed//packWait # Total time passed divided by time necesasry to pass is how many new packs you get

    db[str(id)+"p"]+=int(extraPacks) # add the new packs on

    if db[str(id)+"p"]>10:
      db[str(id)+"p"]= 10 # If you overload on free packs, reset to 10
      db[str(id)+"t"] = time # Also, set new timer start from here
    elif db[str(id)+"p"]>0:
      # You have not overloaded, you are fine
      db[str(id)+"t"] = int(time + (timePassed % packWait) - packWait) # Set new timer to a few minutes ago when the newest pack stopped counting

      # Check out this last line of code
      # Ensure that running 'c.card' multiple times does not decrease time for next card

    # If you didnt get any packs, nothing changes

  except:
    db[str(id)+"p"]=10
    db[str(id)+"t"]=time


def freePacks2(id, time):
  try:
    timePassed = time-db[str(id)+"t"] # Time passed
    extraPacks = int(timePassed//packWait) # Total time passed divided by time necesasry to pass is how many new packs you get

    if extraPacks!=0:
      db[str(id)+"p"]+=int(extraPacks) # add the new packs on
      if db[str(id)+"p"] >= 10:
        db[str(id)+"p"] = 10
        db[str(id)+"t"] = time
      else:
        db[str(id)+"t"] = db[str(id)+"t"] = int(time + (timePassed % packWait) - packWait)

  except:
    db[str(id)+"p"]=10
    db[str(id)+"t"]=time


def updatePacks(id, num):
  try:
    db[str(id)+"p"] =  int(db[str(id)+"p"] + num)
    return True
  except:
    db[str(id)+"p"] = 0
    return False
  pass


def getCollection(id):
  try:

    return db[str(id)+"c"]
  except:
    return {}

def addToCollection(id, card):


  try:
    col=db[str(id)+"c"]

    try:
      # db[str(id)+"c"][card.name]=db[str(id)+"c"][card.name]+int(1)
      col[card.name]=col[card.name]+int(1)
 
    except:
      # db[str(id)+"c"][card.name]=int(1)
      col[card.name]=int(1)



    db[str(id)+"c"]=col

  except:
    db[str(id)+"c"]={}
    db[str(id)+"c"][card.name]=int(1)

