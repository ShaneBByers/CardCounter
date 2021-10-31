from enum import Enum

from Player import *
from Hand import *
from Shoe import Shoe

class Table:
    def __init__(self, init_number_of_players, init_number_of_decks, verbose):
        self.dealer = Player(True, 0)
        self.players = []
        for i in range(init_number_of_players):
            player = Player(False, i + 1)
            self.players.append(player)
        self.shoe = Shoe(init_number_of_decks)
        self.verbose = verbose

    def play_hand(self):
        self.start_deal()
        self.continue_deal()
        self.end_deal()

    def start_deal(self):
        for player in self.players:
            self.add_card_to_player(player)
        
        self.add_card_to_player(self.dealer, False)

        for player in self.players:
            self.add_card_to_player(player)
        
        self.add_card_to_player(self.dealer)

        if self.verbose:
            print("END OF START:")
            print(self)

    def continue_deal(self):
        while self.has_any_active():
            for player in self.players:
                while player.get_is_continuous_deal():
                    self.add_card_to_player(player)
                if player.hands[0].status == HandStatus.Active:
                    self.add_card_to_player(player)

        if self.verbose:
            print("END OF CONTINUE:")
            print(self)

    def end_deal(self):
        for hand in self.dealer.hands:
            for card in hand.cards:
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
        player.add_card(card, self.dealer.hands[0])
        
        if self.verbose:
            print("MIDDLE OF CONTINUE:")
            print(self)

    def __str__(self):
        table_str = "--- TABLE ---\n\n"
        table_str += str(self.dealer) + "\n"
        for player in self.players:
            table_str += str(player) + "\n"
        table_str += str(self.shoe)
        table_str += "\n--- TABLE ---\n"
        return table_str
