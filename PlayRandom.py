from Game import Game
from Enums import PlayerStyle

player_styles = [PlayerStyle.Counting, PlayerStyle.Optimal, PlayerStyle.Average, PlayerStyle.Random]
number_of_decks = 1
number_of_hands = 10000
verbose = False

game = Game("History.txt")
game.play_random(player_styles, number_of_decks, number_of_hands, verbose)
