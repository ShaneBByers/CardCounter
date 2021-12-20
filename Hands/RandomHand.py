from Hands.HandBase import HandBase
from Enums import *
import random
import sys


class RandomHand(HandBase):

    def __init__(self, init_is_from_split, init_cards=None):
        super().__init__(init_is_from_split, init_cards)
        self.player_choice_randomizer = random.Random()
        self.player_choice_randomizer.seed(random.randrange(sys.maxsize))

    def get_status(self, dealer_hand):
        super_status = super().get_status(dealer_hand)
        if super_status is not None:
            return super_status
        else:
            hand_values = self.get_hand_values(True)
            if hand_values[0] == 21:
                return HandStatus.Stand
            elif len(self.cards) < 2:
                return HandStatus.Active

        return self.player_choice_randomizer.choice([HandStatus.Active, HandStatus.Stand])

    def get_needs_split(self, dealer_hand_values):
        if len(self.cards) != 2:
            return False
        first_value = self.cards[0].get_values()[-1]
        second_value = self.cards[1].get_values()[-1]
        if first_value != second_value:
            return False

        return self.player_choice_randomizer.choice([True, False])

    def get_double_down(self, dealer_hand_values):
        if len(self.cards) != 2:
            return False
        if self.status != HandStatus.Active:
            return False

        return self.player_choice_randomizer.choice([True, False])

    def set_true_count(self, true_count):
        return

    def set_current_bet(self, true_count):
        self.current_bet = self.player_choice_randomizer.randint(10, 100)
