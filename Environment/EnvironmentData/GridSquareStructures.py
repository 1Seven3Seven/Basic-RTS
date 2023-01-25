from enum import Enum, auto


class GridSquareStructures(Enum):
    """
The structures that each grid can have.
    """

    NONE = auto()

    TREE = auto()
    STONE = auto()

    PLAYER_BASE = auto()

    WOOD_WALL = auto()
    STONE_WALL = auto()

    WOOD_SPAWNER = auto()
    STONE_SPAWNER = auto()
