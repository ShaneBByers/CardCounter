from Hands.DealerHand import DealerHand
from Hands.RandomHand import RandomHand
from Hands.AverageHand import AverageHand
from Hands.OptimalHand import OptimalHand
from Hands.CountingHand import CountingHand
from Enums import *


class Player:
    def __init__(self, init_player_style, init_position):
        self.player_style = init_player_style
        self.position = init_position
        self.hands = [self.get_new_hand(False)]
        self.money = 0

    def add_card(self, card, dealer_hand):
        for hand in self.hands:
            if hand.is_continuous_deal or hand.status == HandStatus.Active:
                hand.add_card(card, dealer_hand)
                if hand.needs_split:
                    copy_card = hand.cards[1]
                    hand.cards = [hand.cards[0]]
                    hand.needs_split = False
                    self.hands.append(self.get_new_hand(True, [copy_card]))
                elif hand.double_down:
                    hand.bet *= 2
                return
    
    def pay_results(self, dealer_hand):
        for hand in self.hands:
            self.money += hand.get_pay_result(dealer_hand)
            
    def end_deal(self):
        self.hands = [self.get_new_hand(False)]
        
    def get_is_continuous_deal(self):
        for hand in self.hands:
            if hand.is_continuous_deal:
                return True
        return False

    def get_new_hand(self, is_from_split, card_list=None):
        hand = None
        if self.player_style == PlayerStyle.Dealer:
            hand = DealerHand(is_from_split)
        elif self.player_style == PlayerStyle.Random:
            hand = RandomHand(is_from_split)
        elif self.player_style == PlayerStyle.Average:
            hand = AverageHand(is_from_split)
        elif self.player_style == PlayerStyle.Optimal:
            hand = OptimalHand(is_from_split)
        elif self.player_style == PlayerStyle.Counting:
            hand = CountingHand(is_from_split)
        if hand is not None and card_list is not None:
            hand.cards = card_list
        return hand

    def __str__(self):
        if self.player_style == PlayerStyle.Dealer:
            player_str = "DEALER: "
        else:
            player_str = "PLAYER " + str(self.position) + " - $" + str(self.money) + ": "
            
        for hand in self.hands:
            player_str += str(hand)

        player_str += "\n"

        return player_str
