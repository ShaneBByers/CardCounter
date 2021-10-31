from Hands.HandBase import HandBase
from Enums import *


class DealerHand(HandBase):

    def get_status(self, dealer_hand):
        hand_values = self.get_hand_values(True)
        for hand_value in hand_values:
            if 17 <= hand_value <= 21:
                return HandStatus.Stand
        return HandStatus.Active

    def get_needs_split(self, dealer_hand_values):
        return False

    def get_double_down(self, dealer_hand_values):
        return False
