from Deck import Deck

import random


class Shoe:

    def __init__(self, number_of_decks):
        self.decks = []
        for i in range(number_of_decks):
            deck = Deck(i)
            self.decks.append(deck)
        self.available_cards = []
        self.shuffle()
        self.total_card_count = len(self.available_cards)

    def shuffle(self):
        self.available_cards = [card for deck in self.decks for card in deck.cards]
        random.shuffle(self.available_cards)

    def next_card(self, is_shown):
        card = self.available_cards.pop()
        card.is_shown = is_shown
        return card

    def __str__(self):
        shoe_str = "SHOE USED     : " + str(self.total_card_count - len(self.available_cards)) + "\n"
        shoe_str += "SHOE AVAILABLE: " + str(len(self.available_cards)) + "\n"
        return shoe_str
