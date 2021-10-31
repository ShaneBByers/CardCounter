from Deck import Deck

import random


class Shoe:

    def __init__(self, number_of_decks):
        self.decks = []
        for i in range(number_of_decks):
            deck = Deck(i)
            self.decks.append(deck)
        self.available_cards = [card for deck in self.decks for card in deck.cards]
        self.current_cards = []
        self.discarded_cards = []
        self.shuffle()
        self.total_card_count = len(self.available_cards)

    def shuffle(self):
        random.shuffle(self.available_cards)

    def next_card(self, is_shown):
        card = self.available_cards.pop()
        card.is_shown = is_shown
        self.current_cards.append(card)
        if len(self.available_cards) == 0:
            self.available_cards = self.discarded_cards
            self.discarded_cards = []
            self.shuffle()
        return card
    
    def end_deal(self):
        self.discarded_cards.extend(self.current_cards)
        self.current_cards = []

    def __str__(self):
        shoe_str = "SHOE CURRENT  : " + str(len(self.current_cards)) + "\n"
        shoe_str += "SHOE DISCARDED: " + str(len(self.discarded_cards)) + "\n"
        shoe_str += "SHOE AVAILABLE: " + str(len(self.available_cards)) + "\n"
        return shoe_str
