from Hands.HandBase import HandBase
from Enums import *


class DealerHand(HandBase):

    def get_status(self, dealer_hand):
        hand_values = self.get_hand_values(True)
        if hand_values[0] > 21:
            return HandStatus.Bust
        for hand_value in hand_values:
            if 17 <= hand_value <= 21:
                return HandStatus.Stand
        return HandStatus.Active

    def get_needs_split(self, dealer_hand_values):
        return False

    def get_double_down(self, dealer_hand_values):
        return False

    def set_true_count(self, true_count):
        return

    def set_current_bet(self, true_count):
        return
