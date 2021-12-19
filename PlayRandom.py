from Game import Game
from Enums import PlayerStyle

player_styles = [PlayerStyle.Random, PlayerStyle.Optimal, PlayerStyle.Average]
number_of_decks = 6
number_of_hands = 100000
verbose = False

game = Game("History.txt")
game.play_random(player_styles, number_of_decks, number_of_hands, verbose)