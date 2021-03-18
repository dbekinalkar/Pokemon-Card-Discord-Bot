
rarities = ["exclusive","rare holo", "rare", "uncommon", "common"]
cards = []

class PokemonCard:

  def __init__(self, num, name, rarity, imgurl):
    self.num = num
    self.name = name
    self.rarity = rarity  
    self.imgurl = imgurl


def initializeCards():
  file = open("Card Info 1.csv", "r")

  for line in file:
    list = line.strip().split(",")
    c = PokemonCard(list[0], list[1], list[2], list[3])


    cards.append(c)

  file.close()

def byRarity(cardList, rarity):
  cardsByRarity = []
  for card in cardList:
    if card.rarity.lower() == rarity.lower():
      cardsByRarity.append(card)

  return cardsByRarity

def getCard(cardName):

  for card in cards:
    if cardName.lower() == card.name.lower():
      return card

  return None


