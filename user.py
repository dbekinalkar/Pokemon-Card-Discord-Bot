from replit import db
from datetime import datetime
from datetime import timedelta

# Problem with Code: Cannot store User object into the databse
# Solution: Make the keys in the database just be DiscordID + "rolls" or "counter" or "collection"
# Also create just 1 list of all cards, makes it easier to look through when necessary
#   How: Recode that part so that the code for choosing a rare card will instead choose from a list of 1-16 for holo rare, 17-32 for rare, etc
# Also, when storing collection, make a dictionary of card_name:multiples_of_card
#   Prob wont be able to store card objects

class User:

  rollWait = timedelta(minutes=10) 


  def __init__(self, timeCalled):
    self.rolls = 10
    self.timeCounter = timeCalled

    self.collection = {}


def collectionAdd(userVar, cardVar):
  if userVar.collection.get(cardVar.name) == None :
    userVar.collection[cardVar.name] = [cardVar, 1]
  else:
    userVar.collection.get(cardVar.name)[1] += 1


def updateRolls(author, timeCalled):
  try:
    userVar = db[str(author.id)]
    extraRolls = (timeCalled - userVar.timeCounter) // User.rollWait
    if (userVar.rolls+extraRolls) > 10:
      userVar.timeCounter = timeCalled
      userVar.rolls = 10

    elif extraRolls > 0:
      remainderTime = (timeCalled - userVar.timeCounter) % User.rollWait
      userVar.timeCounter = timeCalled - remainderTime
      userVar.rolls += extraRolls

    
  except Exception:
    db[str(author.id)] = User(timeCalled=timeCalled)
    print(Exception)

  return db[author.id].rolls
