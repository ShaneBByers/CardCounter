import Constants


class Card:

    def __init__(self, init_number, init_suit):
        self.number = init_number
        self.suit = init_suit
        self.is_shown = False

    def __str__(self):
        if self.is_shown:
            card_str = self.number + self.suit
        else:
            card_str = "**"

        return card_str

    def get_values(self):
        return Constants.CARD_NUMBER_VALUES[self.number]