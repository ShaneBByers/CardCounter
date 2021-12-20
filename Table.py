from Player import Player
from Shoe import Shoe
from Enums import *


class Table:
    def __init__(self, player_styles, init_number_of_decks, verbose):
        self.dealer = Player(PlayerStyle.Dealer, 0)
        self.players = []
        for i in range(len(player_styles)):
            player = Player(player_styles[i], i + 1)
            self.players.append(player)
        self.shoe = Shoe(init_number_of_decks)
        self.verbose = verbose
        self.current_count = 0

    def play_hand(self):
        self.start_deal()
        self.continue_deal()
        self.end_deal()

    def start_deal(self):
        for player in self.players:
            player.set_current_bet(self.get_true_count())

        for player in self.players:
            self.add_card_to_player(player)
        
        self.add_card_to_player(self.dealer)

        for player in self.players:
            self.add_card_to_player(player)
        
        self.add_card_to_player(self.dealer, False)

        if self.verbose:
            print("END OF START:")
            print(self)

    def continue_deal(self):
        while self.has_any_active():
            for player in self.players:
                while player.get_is_continuous_deal():
                    self.add_card_to_player(player)
                else:
                    self.add_card_to_player(player)

        if self.verbose:
            print("END OF CONTINUE:")
            print(self)

    def end_deal(self):
        for hand in self.dealer.hands:
            for card in hand.cards:
                if not card.is_shown:
                    card_value = card.get_values()[-1]
                    if card_value >= 10:
                        self.current_count -= 1
                    elif card_value <= 6:
                        self.current_count += 1
                card.is_shown = True

        while self.dealer.hands[0].status == HandStatus.Active:
            self.add_card_to_player(self.dealer)
        
        for player in self.players:
            player.pay_results(self.dealer.hands[0])

        if self.verbose:
            print("END OF END:")
        print(self)
        
        self.shoe.end_deal()
        
        self.dealer.end_deal()
        
        for player in self.players:
            player.end_deal()

    def has_any_active(self):
        for player in self.players:
            for hand in player.hands:
                if hand.status == HandStatus.Active:
                    return True
        return False

    def add_card_to_player(self, player, is_shown=True):
        card = self.shoe.next_card(is_shown)
        if self.shoe.just_shuffled:
            self.current_count = 0
            self.shoe.just_shuffled = False
        elif is_shown:
            card_value = card.get_values()[-1]
            if card_value >= 10:
                self.current_count -= 1
            elif card_value <= 6:
                self.current_count += 1
        player.add_card(card, self.dealer.hands[0], self.get_true_count())
        
        if self.verbose:
            print("MIDDLE OF CONTINUE:")
            print(self)

    def get_true_count(self):
        return float(self.current_count) / self.shoe.get_remaining_decks()

    def __str__(self):
        table_str = "--- TABLE ---\n\n"
        table_str += str(self.dealer) + "\n"
        for player in self.players:
            table_str += str(player) + "\n"
        table_str += str(self.shoe)
        table_str += "CURRENT COUNT: " + str(self.current_count)
        table_str += "\n--- TABLE ---\n"
        return table_str
