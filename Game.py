import random
import sys
import os
from Table import Table
from Enums import *


class Game:
    def __init__(self, history_file_name):
        self.history_file_path = os.path.dirname(os.path.realpath(__file__)) + "/" + history_file_name
        self.table = None

    def play_random(self, player_styles, number_of_decks, number_of_hands, logging_type):
        seed = random.randrange(sys.maxsize)
        self.write_config(player_styles, number_of_decks, number_of_hands, seed)
        self.play_game(player_styles, number_of_decks, number_of_hands, seed, logging_type)

    def replay_last(self, verbose):
        (player_styles, number_of_decks, number_of_hands, seed) = self.read_config()
        self.play_game(player_styles, number_of_decks, number_of_hands, seed, verbose)

    def play_game(self, player_styles, number_of_decks, number_of_hands, seed, logging_type):
        random.seed(seed)
        self.table = Table(player_styles, number_of_decks, logging_type)
        for _ in range(number_of_hands):
            self.table.play_hand()
        print(self)

    def write_config(self, player_styles, number_of_decks, number_of_hands, seed):
        config_str = ""
        for player_style in player_styles:
            config_str += str(player_style.value)
        config_str += "|" + str(number_of_decks) + "|" + str(number_of_hands) + "|" + str(seed) + "\n"

        with open(self.history_file_path, "a+") as history_file:
            history_file.write(config_str)

    def read_config(self):
        with open(self.history_file_path, "r") as history_file:
            last_line = history_file.readlines()[-1]

        game_components = last_line.split("|")

        player_styles = []
        player_styles_str = game_components[0]
        for player_style_char in player_styles_str:
            player_style = PlayerStyle(int(player_style_char))
            player_styles.append(player_style)
        decks = int(game_components[1])
        hands = int(game_components[2])
        seed = int(game_components[3])
        return player_styles, decks, hands, seed

    def __str__(self):
        game_str = "--- GAME ---\n"
        for player in self.table.players:
            if player.player_style != PlayerStyle.Dealer:
                player_sign = "+" if player.money >= 0 else "-"
                player_str = "PLAYER " + \
                             str(player.position) + \
                             " - " + \
                             str(player.player_style.name) + \
                             " - " + \
                             player_sign + \
                             "${:,.2f}".format(abs(player.money))
                game_str += player_str + "\n"
        game_str += "--- GAME ---"
        return game_str
