from enum import Enum


class HandStatus(Enum):
    Active = 0
    Blackjack = 1
    Stand = 3
    Bust = 4


class HandResult(Enum):
    StillActive = -99999999999999999999999999
    Blackjack = 1.5
    Win = 1
    Lose = -1
    Tie = 0


class PlayerStyle(Enum):
    Dealer = 0
    Random = 1
    Average = 2
    Optimal = 3
    Counting = 4


class LoggingType(Enum):
    AllInfo = 0
    OnlyEndOfHands = 1
    OnlyEndOfGame = 2
