
class PokemonCard:

  def __init__(self, num, name, rarity):
    self.num = num
    self.name = name
    self.rarity = rarity  
    self.imgurl = "https://images.pokemontcg.io/base1/"+num+"_hires.png"

# cardsByRarity = {"rare holo":[], "rare":[], "uncommon":[], "common":[]} # Replaced with function "byRarity"

cards = []


def initializeCards():
  file = open("Card Info.csv", "r")

  for line in file:
    list = line.strip().split(",")
    c = PokemonCard(list[0], list[1], list[2])
    # cardsByRarity.get(c.rarity.lower()).append(c) # Replaced with function "byRarity"

    cards.append(c)

  file.close()

def byRarity(rarity):
  cardsByRarity = []
  for card in cards:
    if card.rarity.lower() == rarity.lower():
      cardsByRarity.append(card)

  return cardsByRarity

def getCard(cardName):
  #for cardType in cards:
  #  for card in cardType:
  #    if cardName.lower() == card.name.lower():
  #      return card

  for card in cards:
    if cardName.lower() == card.name.lower():
      return card

  return None


