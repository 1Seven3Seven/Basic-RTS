from enum import Enum


class GridSquareStructures(Enum):
    """
The structures that each grid can have.
    """

    # Additional attributes
    weight: int

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1

        obj = object.__new__(cls)
        obj._value_ = value

        return obj

    def __init__(self, weight: int):
        self.weight = weight

    NONE = 0

    TREE = 1
    STONE = 1

    PLAYER_BASE = 0

    WOOD_WALL = 8
    STONE_WALL = 12

    WOOD_SPAWNER = 0
    STONE_SPAWNER = 0
