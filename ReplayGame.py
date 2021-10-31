from Table import Table
import random
import os

history_file = open(os.path.dirname(os.path.realpath(__file__)) + "/History.txt", "r")
last_line = history_file.readlines()[-1]
history_file.close()

game_components = last_line.split("|")

players = int(game_components[0])
decks = int(game_components[1])
hands = int(game_components[2])
seed = int(game_components[3])

random.seed(seed)

table = Table(players, decks, True)
for _ in range(hands):
    table.play_hand()