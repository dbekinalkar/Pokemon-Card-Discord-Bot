from replit import db



packWait = 300 # Seconds

def getPacks(id):
  try:
    return db[str(id)+"p"]
  except:
    db[str(id)+"p"] = 0
    return 0

def freePacks(id, time):
  try:
    timePassed = time-db[str(id)+"t"]
    extraPacks = timePassed//packWait

    db[str(id)+"p"]+=extraPacks

    if db[str(id)+"p"]>10:
      db[str(id)+"p"]=10
      db[str(id)+"t"] = time
    elif db[str(id)+"p"]>0:
      db[str(id)+"t"] = time + (timePassed % packWait) - packWait

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

