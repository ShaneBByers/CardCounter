from Hands.HandBase import HandBase
from Enums import *


class AverageHand(HandBase):

    def get_status(self, dealer_hand):
        super_status = super().get_status(dealer_hand)
        if super_status is not None:
            return super_status
        else:
            hand_values = self.get_hand_values(True)
            if len(hand_values) > 1:
                if hand_values[0] >= 18:
                    return HandStatus.Stand
            else:
                if hand_values[0] >= 12:
                    return HandStatus.Stand
        return HandStatus.Active

    def get_needs_split(self, dealer_hand_values):
        if len(self.cards) == 2:
            first_value = self.cards[0].get_values()[-1]
            second_value = self.cards[1].get_values()[-1]
            if first_value == second_value and 7 <= first_value <= 9:
                return True
        return False

    def get_double_down(self, dealer_hand_values):
        if len(self.cards) == 2:
            total_value = 0
            for card in self.cards:
                total_value += card.get_values()[-1]
            if total_value == 11:
                return True
        return False
