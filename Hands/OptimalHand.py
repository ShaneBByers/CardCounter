from Hands.HandBase import HandBase
from Enums import *


class OptimalHand(HandBase):

    def get_status(self, dealer_hand):
        hand_values = self.get_hand_values(True)
        if hand_values[0] == 21 and len(self.cards) == 2 and not self.is_continuous_deal:
            return HandStatus.Blackjack
        elif self.is_continuous_deal and len(self.cards) == 2 and self.cards[0].get_values()[-1] == 11:
            return HandStatus.Stand
        elif self.double_down and len(self.cards) == 3:
            return HandStatus.Stand
        elif hand_values[0] > 21:
            return HandStatus.Bust
        else:
            dealer_hand_values = dealer_hand.get_hand_values(False)
            if len(hand_values) > 1:
                if max(dealer_hand_values) >= 9:
                    if hand_values[1] >= 19:
                        return HandStatus.Stand
                elif max(dealer_hand_values) >= 2:
                    if hand_values[1] >= 18:
                        return HandStatus.Stand
            else:
                if max(dealer_hand_values) >= 7:
                    if hand_values[0] >= 17:
                        return HandStatus.Stand
                elif max(dealer_hand_values) >= 4:
                    if max(hand_values) >= 12:
                        return HandStatus.Stand
                elif max(dealer_hand_values) >= 2:
                    if max(hand_values) >= 13:
                        return HandStatus.Stand
        return HandStatus.Active

    def get_needs_split(self, dealer_hand_values):
        if len(self.cards) == 2:
            first_value = self.cards[0].get_values()[-1]
            second_value = self.cards[1].get_values()[-1]
            if first_value == second_value:
                dealer_value = dealer_hand_values[-1]
                if first_value == 11 or first_value == 8:
                    return True
                elif first_value == 9:
                    if dealer_value <= 6 or 8 <= dealer_value <= 9:
                        return True
                elif first_value == 7 or first_value == 3 or first_value == 2:
                    if dealer_value <= 7:
                        return True
                elif first_value == 6:
                    if dealer_value <= 6:
                        return True
                elif first_value == 4:
                    if 5 <= dealer_value <= 6:
                        return True
        return False

    def get_double_down(self, dealer_hand_values):
        if (len(self.cards) == 1 and self.is_continuous_deal) or len(self.cards) == 2:
            total_value = 0
            for card in self.cards:
                total_value += card.get_values()[-1]
            if total_value == 11:
                return True
            dealer_value = dealer_hand_values[-1]
            if total_value == 10 and dealer_value <= 9:
                return True
            if total_value == 9 and 3 <= dealer_value <= 6:
                return True
            if len(self.cards) == 2 and dealer_value <= 6:
                first_value = self.cards[0].get_values()[-1]
                second_value = self.cards[1].get_values()[-1]
                min_value = min(first_value, second_value)
                max_value = max(first_value, second_value)
                if dealer_value >= 3 and min_value == 6 and max_value == 11:
                    return True
                if dealer_value >= 4 and 4 <= min_value <= 5 and max_value == 11:
                    return True
                if dealer_value >= 5 and 2 <= min_value <= 3 and max_value == 11:
                    return True
        return False
