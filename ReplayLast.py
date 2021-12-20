from Game import Game
from Enums import LoggingType

logging_type = LoggingType.AllInfo

game = Game("History.txt")
game.replay_last(logging_type)
