from enum import Enum

class Direction(Enum):
    BUY = 1
    SELL = -1

class OrderType(Enum):
    SUBMISSION = 1
    CANCELLATION = 2
    DELETION = 3
    EXECUTION_VISIBLE = 4
    EXECUTION_HIDDEN = 5
    TRADING_HALT = 7