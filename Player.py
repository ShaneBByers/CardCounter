from Hand import *

class Player:
    def __init__(self, init_is_dealer, init_position):
        self.is_dealer = init_is_dealer
        self.position = init_position
        self.hands = [Hand(1, self.is_dealer, False)]
        self.money = 0

    def add_card(self, card, dealer_hand):
        for hand in self.hands:
            if hand.is_continuous_deal or hand.status == HandStatus.Active:
                hand.add_card(card, dealer_hand)
                if hand.needs_split:
                    self.hands.append(Hand(1, self.is_dealer, True))
                    copy_card = hand.cards[1]
                    hand.cards = [hand.cards[0]]
                    hand.needs_split = False
                    self.hands[-1].cards = [copy_card]
                return
    
    def pay_results(self, dealer_hand):
        for hand in self.hands:
            self.money += hand.get_pay_result(dealer_hand)
            
    def end_deal(self):
        self.hands = [Hand(1, self.is_dealer, False)]
        
    def get_is_continuous_deal(self):
        for hand in self.hands:
            if hand.is_continuous_deal:
                return True
        return False

    def __str__(self):
        if self.is_dealer:
            player_str = "DEALER: "
        else:
            player_str = "PLAYER " + str(self.position) + " - $" + str(self.money) + ": "
            
        for hand in self.hands:
            player_str += str(hand)

        player_str += "\n"

        return player_str
