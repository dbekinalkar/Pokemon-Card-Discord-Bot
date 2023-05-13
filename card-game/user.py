import time


class Collection:
    def __init__(self):
        self.col = {}

    def add(self, card, n=1):
        if card not in self.col.keys():
            self.col[card] = 0
        self.col[card] += n

    def remove(self, card):
        if card not in self.col.keys():
            return
        self.col[card] = 0

    def subtract(self, card, n=1):
        if card not in self.col.keys() or self.col[card] < n:
            raise Exception('Underflow Error: Not enough cards in collection')
        self.col[card] -= n


class User:
    max_packs = 10
    pack_wait_time = 600 # 600 seconds = 10 minutes

    def __init__(self):
        self.time = time.time()
        self.packs = User.max_packs
        self.col = Collection()

    def update_packs(self, time):
        time_passed = time - self.time
        extra_packs = int(time_passed // User.pack_wait_time)

        if extra_packs == 0:
            return
        elif extra_packs + self.packs >= User.max_packs:
            self.packs = User.max_packs
            self.time = time
        else:
            self.packs += extra_packs
            self.time = self.time + extra_packs * User.pack_wait_time

    def open_pack(self) -> str:
        self.update_packs(time.time())

        if self.packs <= 0:
            raise Exception('Underflow Error: Not enough packs')

        card = randomcard()
        self.col.add(card)
        return card

