import Constants
from Card import Card


class Deck:

    def __init__(self, init_deck_number):
        self.deck_number = init_deck_number
        self.cards = []
        for card_suit in Constants.CARD_SUITS:
            for card_number in Constants.CARD_NUMBER_VALUES.keys():
                card = Card(card_number, card_suit)
                self.cards.append(card)

    def __str__(self):
        deck_string = "--- DECK " + str(self.deck_number + 1) + " --- \n"
        for card in self.cards:
            deck_string += str(card) + "\n"
        deck_string += "--- DECK " + str(self.deck_number + 1) + " --- \n"

        return deck_string
