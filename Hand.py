from enum import Enum

class HandStatus(Enum):
    Active = 0
    Blackjack = 1
    Stand = 3
    Bust = 4
    
class HandResult(Enum):
    StillActive = -99999
    Blackjack = 1.5
    Win = 1
    Lose = -1
    Tie = 0

class Hand:
    def __init__(self, init_bet, init_is_dealer_hand):
        self.is_dealer_hand = init_is_dealer_hand
        self.status = HandStatus.Active
        self.result = HandResult.StillActive
        self.bet = init_bet
        self.cards = []
        self.is_splitting = False
    
    def add_card(self, card, dealer_hand):
        self.cards.append(card)
        self.status = self.get_status(dealer_hand)
        self.is_splitting = self.get_is_splitting(dealer_hand.get_hand_values(False))
            
    def get_status(self, dealer_hand):
        hand_values = self.get_hand_values(True)
        if hand_values[0] == 21 and len(self.cards) == 2 and not self.is_splitting:
            return HandStatus.Blackjack
        elif self.is_splitting and len(self.cards) == 2 and self.cards[0].get_values()[-1] == 11:
            return HandStatus.Stand
        elif hand_values[0] > 21:
            return HandStatus.Bust
        elif self.is_dealer_hand:
            for hand_value in hand_values:
                if 17 <= hand_value <= 21:
                    return HandStatus.Stand
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
            elif possible_value not in return_values:
                return_values.append(possible_value)

        return sorted(return_values)
    
    def get_is_splitting(self, dealer_hand_values):
        if self.is_dealer_hand:
            return False
        elif len(self.cards) == 2:
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
        elif self.status == HandStatus.Active and self.is_splitting:
            return True
        return False
    
    def get_pay_result(self, dealer_hand):
        self.result = self.get_result(dealer_hand)
        return self.bet * self.result.value
        
    def get_result(self, dealer_hand):
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
    
    def __str__(self):
        hand_str = ""
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
            hand_str += " - WIN"
        elif self.result == HandResult.Lose:
            hand_str += " - LOSE"
        elif self.result == HandResult.Tie:
            hand_str += " - TIE"
        
        return hand_str
