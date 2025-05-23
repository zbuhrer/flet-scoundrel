import random
from typing import Optional
from card_data import CardData

class GameState:
    def __init__(self):
        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.health = 20
        self.power = 0
        self.enemies = []  # List of CardData instances (enemies)
        self.equipped_class: Optional[CardData] = None  # Track equipped class (CardData)
        self.equipped_weapon: Optional[CardData] = None #Track equipped weapon (CardData)

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
        if self.health < 0:
            self.health = 0

    def apply_healing(self, amount):
        self.health = min(self.health + amount, 20) # Assuming max health is 20

    def equip_class(self, card):
        """Equips a red face card, granting a bonus."""
        if card.suit in ("Hearts", "Diamonds") and card.rank in ("Jack", "Queen", "King"):
            self.equipped_class = card
            print(f"Equipped {card.name} as class.")
        else:
            print("Cannot equip this card as a class.")
