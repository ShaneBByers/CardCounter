from Player import *
from Shoe import Shoe


class Table:
    def __init__(self, init_number_of_players, init_number_of_decks):
        self.dealer = Player(True, 0)
        self.players = []
        for i in range(init_number_of_players):
            player = Player(False, i + 1)
            self.players.append(player)
        self.shoe = Shoe(init_number_of_decks)

    def play_hand(self):
        self.start_deal()
        self.continue_deal()
        self.end_deal()

    def start_deal(self):
        self.add_card_to_player(self.dealer, False)

        for player in self.players:
            self.add_card_to_player(player)

        self.add_card_to_player(self.dealer)

        for player in self.players:
            self.add_card_to_player(player)

        print("END OF START:")
        print(self)

    def continue_deal(self):
        while self.has_any_active():
            for player in self.players:
                if player.status == PlayerStatus.Active:
                    player.update_status(self.dealer)
                    if player.status == PlayerStatus.Active:
                        self.add_card_to_player(player)

        print("END OF CONTINUE:")
        print(self)

    def end_deal(self):
        self.dealer.status = PlayerStatus.Active

        for card in self.dealer.hand:
            card.is_shown = True

        while self.dealer.status == PlayerStatus.Active:
            self.dealer.update_status(self.dealer)
            if self.dealer.status == PlayerStatus.Active:
                self.add_card_to_player(self.dealer)

        print("END OF END:")
        print(self)

    def has_any_active(self):
        for player in self.players:
            if player.status is PlayerStatus.Active:
                return True
        return False

    def add_card_to_player(self, player, is_shown=True):
        card = self.shoe.next_card(is_shown)
        player.add_card(card)

    def __str__(self):
        table_str = "--- TABLE ---\n\n"
        table_str += str(self.dealer) + "\n"
        for player in self.players:
            table_str += str(player) + "\n"
        table_str += str(self.shoe)
        table_str += "\n--- TABLE ---\n"
        return table_str
