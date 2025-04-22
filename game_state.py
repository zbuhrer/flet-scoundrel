import random

class GameState:
    def __init__(self):
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.health = 20
        self.power = 0
        self.enemies = []  # We can define an Enemy class later

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        if not self.deck:
            self.deck = self.discard_pile[:]  # Copy the discard pile
            self.discard_pile = []
            self.shuffle_deck()
            if not self.deck: # Still empty?  No cards left!
                return None # Or raise an exception, depending on desired behavior
        card = self.deck.pop()
        self.hand.append(card)
        return card

    def draw_hand(self, num_cards=5):
        for _ in range(num_cards):
            card = self.draw_card()
            if card is None:
                break # No more cards to draw

    def discard_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            self.discard_pile.append(card)

    def apply_damage(self, amount):
        self.health -= amount

    def apply_healing(self, amount):
        self.health = min(self.health + amount, 20) # Assuming max health is 20
