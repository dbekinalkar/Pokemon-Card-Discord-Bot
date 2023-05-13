class Card:
    rarities = {"exclusive": "✧", "rare holo": "☆", "rare": "★", "uncommon": "◆", "common": "⬤"}

    def __init__(self, num, name, rarity, imgurl):
        self.num = num
        self.name = name
        self.rarity = rarity
        self.imgurl = imgurl


cards = []


def initializeCards():
    with open('card_info.csv', 'r') as file:
        global cards
        cards = [Card(ctx[0], ctx[1], ctx[2], ctx[3]) for ctx in (line.strip().split(",") for line in file)]


def byRarity(card_list, rarity):
    cards_rarity = [card for card in cards if card.rarity.lower() == rarity.lower()]
    return cards_rarity


def getCard(name):
    if name == "":
        return cards[0]

    for card in cards:
        if name.lower() == card.name.lower():
            return card

    return None
