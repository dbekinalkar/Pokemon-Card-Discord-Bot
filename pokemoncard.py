
class PokemonCard:

  def __init__(self, num, name, rarity):
    self.num = num
    self.name = name
    self.rarity = rarity  
    self.imgurl = "https://images.pokemontcg.io/base1/"+num+"_hires.png"

cards = {"rare holo":[], "rare":[], "uncommon":[], "common":[]}

def initializeCards():
  file = open("Card Info.csv", "r")

  for line in file:
    list = line.strip().split(",")
    c = PokemonCard(list[0], list[1], list[2])
    cards.get(c.rarity.lower()).append(c)

  file.close()

