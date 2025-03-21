import abc
from Enums import *


class HandBase(metaclass=abc.ABCMeta):
    def __init__(self, init_is_from_split, init_cards=None):
        self.is_continuous_deal = init_is_from_split
        if init_cards is None:
            self.cards = []
        else:
            self.cards = init_cards
        self.double_down = False
        self.status = HandStatus.Active
        self.result = HandResult.StillActive
        self.pay_result = 0
        self.current_bet = None
    
    def add_card(self, card, dealer_hand, true_count):
        self.cards.append(card)
        self.set_true_count(true_count)
        self.status = self.get_status(dealer_hand)
        if self.is_continuous_deal and self.status != HandStatus.Active:
            self.is_continuous_deal = False

    @abc.abstractmethod
    def get_status(self, dealer_hand):
        hand_values = self.get_hand_values(True)
        if hand_values[0] > 21:
            return HandStatus.Bust
        elif hand_values[0] == 21 and len(self.cards) == 2 and not self.is_continuous_deal:
            return HandStatus.Blackjack
        elif self.is_continuous_deal and len(self.cards) == 2 and self.cards[0].get_values()[-1] == 11:
            return HandStatus.Stand
        elif self.double_down and len(self.cards) == 3:
            return HandStatus.Stand
        return None

    @abc.abstractmethod
    def get_needs_split(self, dealer_hand_values):
        return

    @abc.abstractmethod
    def get_double_down(self, dealer_hand_values):
        return

    @abc.abstractmethod
    def set_true_count(self, true_count):
        return

    @abc.abstractmethod
    def set_current_bet(self, true_count):
        return

    def get_hand_values(self, include_hidden_values):
        possible_values = [0]
        for card in self.cards:
            if include_hidden_values or card.is_shown:
                new_possible_values = []
                for possible_value in possible_values:
                    for card_value in card.get_values():
                        new_possible_values.append(possible_value + card_value)
                possible_values = new_possible_values.copy()

        return_values = []
        for possible_value in possible_values:
            if possible_value == 21 or (possible_value > 21 and len(return_values) == 0):
                return [possible_value]
            elif possible_value not in return_values and possible_value < 21:
                return_values.append(possible_value)

        return sorted(return_values)

    def get_result(self, dealer_hand):
        if self.status == HandStatus.Active:
            raise Exception("UH OH.")
        if self.status == HandStatus.Blackjack:
            if dealer_hand.status == HandStatus.Blackjack:
                return HandResult.Tie
            else:
                return HandResult.Blackjack
        elif self.status == self.status.Stand:
            if dealer_hand.status == HandStatus.Blackjack:
                return HandResult.Lose
            elif dealer_hand.status == HandStatus.Stand:
                player_value = self.get_hand_values(True)[-1]
                dealer_value = dealer_hand.get_hand_values(True)[-1]
                if player_value > dealer_value:
                    return HandResult.Win
                elif player_value < dealer_value:
                    return HandResult.Lose
                else:
                    return HandResult.Tie
            elif dealer_hand.status == HandStatus.Bust:
                return HandResult.Win
        elif self.status == HandStatus.Bust:
            return HandResult.Lose
    
    def get_pay_result(self, dealer_hand):
        self.result = self.get_result(dealer_hand)
        self.pay_result = self.current_bet * self.result.value
        if self.double_down:
            self.pay_result *= 2
        return self.pay_result
    
    def __str__(self):
        hand_str = "\n"
        for card in self.cards:
            hand_str += str(card) + " "
        
        hand_str += "- "

        hand_values = self.get_hand_values(self.result != HandResult.StillActive)
        if self.status == HandStatus.Blackjack:
            hand_str += str(hand_values[0]) + " - BLACKJACK"
        elif self.status == HandStatus.Bust:
            hand_str += str(hand_values[0]) + " - BUST"
        elif self.status == HandStatus.Stand:
            hand_str += str(max(hand_values)) + " - STAND"
        else:
            for i in range(len(hand_values)):
                hand_str += str(hand_values[i])
                if i < len(hand_values) - 1:
                    hand_str += " or "
        
        if self.result == HandResult.Win:
            hand_str += " - WIN (+$" + str(self.pay_result) + ")"
        elif self.result == HandResult.Lose:
            hand_str += " - LOSE (-$" + str(abs(self.pay_result)) + ")"
        elif self.result == HandResult.Tie:
            hand_str += " - TIE"
        elif self.result == HandResult.Blackjack:
            hand_str += " (+$" + str(self.pay_result) + ")"
        
        return hand_str
