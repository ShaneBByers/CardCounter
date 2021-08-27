from enum import Enum


class PlayerStatus(Enum):
    Active = 0
    Blackjack = 1
    Stand = 2
    Bust = 3


class Player:
    def __init__(self, init_is_dealer, init_position):
        self.is_dealer = init_is_dealer
        self.position = init_position
        self.hand = []
        self.status = PlayerStatus.Active

    def update_status(self, dealer):
        player_hand_values = self.get_hand_values()
        if self.is_dealer:
            for player_hand_value in player_hand_values:
                if 17 <= player_hand_value <= 21:
                    self.status = PlayerStatus.Stand
        else:
            dealer_hand_values = dealer.get_hand_values()
            if len(player_hand_values) > 1:
                sorted_player_hand_values = sorted(player_hand_values)
                if max(dealer_hand_values) >= 9:
                    if sorted_player_hand_values[1] >= 19:
                        self.status = PlayerStatus.Stand
                elif max(dealer_hand_values) >= 2:
                    if sorted_player_hand_values[1] >= 18:
                        self.status = PlayerStatus.Stand
            else:
                if max(dealer_hand_values) >= 7:
                    if player_hand_values[0] >= 17:
                        self.status = PlayerStatus.Stand
                elif max(dealer_hand_values) >= 4:
                    if max(player_hand_values) >= 12:
                        self.status = PlayerStatus.Stand
                elif max(dealer_hand_values) >= 2:
                    if max(player_hand_values) >= 13:
                        self.status = PlayerStatus.Stand

    def add_card(self, card):
        self.hand.append(card)
        hand_values = self.get_hand_values()
        if hand_values[0] == 21:
            self.status = PlayerStatus.Blackjack
        elif hand_values[0] > 21:
            self.status = PlayerStatus.Bust

    def get_hand_values(self):
        possible_values = [0]
        for card in self.hand:
            if card.is_shown:
                new_possible_values = []
                for possible_value in possible_values:
                    for card_value in card.get_values():
                        new_possible_values.append(possible_value + card_value)
                possible_values = new_possible_values.copy()

        return_values = []
        for possible_value in possible_values:
            if possible_value == 21:
                return_values = [21]
                break
            if possible_value not in return_values and (possible_value < 21 or len(return_values) == 0):
                return_values.append(possible_value)

        return return_values

    def __str__(self):
        if self.is_dealer:
            player_str = "DEALER: "
        else:
            player_str = "PLAYER " + str(self.position) + ": "

        hand_values = self.get_hand_values()

        if self.status == PlayerStatus.Blackjack:
            player_str += str(hand_values[0]) + " - BLACKJACK"
        elif self.status == PlayerStatus.Bust:
            player_str += str(hand_values[0]) + " - BUST"
        elif self.status == PlayerStatus.Stand:
            player_str += str(max(hand_values)) + " - STAND"
        else:
            for i in range(len(hand_values)):
                player_str += str(hand_values[i])
                if i < len(hand_values) - 1:
                    player_str += " or "

        player_str += "\n"

        for card in self.hand:
            player_str += str(card) + " "

        player_str += "\n"

        return player_str
