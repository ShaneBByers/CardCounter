from Game import Game
from Enums import PlayerStyle, LoggingType

player_styles = [PlayerStyle.Counting, PlayerStyle.Optimal, PlayerStyle.Average, PlayerStyle.Random]
number_of_decks = 6
number_of_hands = 10
logging_type = LoggingType.OnlyEndOfGame

game = Game("History.txt")
game.play_random(player_styles, number_of_decks, number_of_hands, logging_type)
