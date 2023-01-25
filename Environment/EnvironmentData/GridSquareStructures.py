from enum import Enum


class GridSquareStructures(Enum):
    """
The structures that each grid can have.
    """

    # Additional attributes
    weight: int

    def __new__(cls, value: str, weight: int = 0) -> 'GridSquareStructures':
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.weight = weight

        return obj

    NONE = ('None', 0)

    TREE = ('Tree', 1)
    STONE = ('Stone', 1)

    PLAYER_BASE = ('Player Base', 0)

    WOOD_WALL = ('Wood Wall', 8)
    STONE_WALL = ('Stone Wall', 12)

    WOOD_SPAWNER = ('Wood Spawner', 0)
    STONE_SPAWNER = ('Stone Spawner', 0)
