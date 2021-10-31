from Table import Table
import random
import sys
import os

players = 4
decks = 6
hands = 1
seed = random.randrange(sys.maxsize)

random.seed(seed)

table = Table(players, decks, True)
for _ in range(hands):
    table.play_hand()

game_str = str(players) + "|" + str(decks) + "|" + str(hands) + "|" + str(seed)

history_file = open(os.path.dirname(os.path.realpath(__file__)) + "/History.txt", "a+")
history_file.write(game_str)
history_file.close()