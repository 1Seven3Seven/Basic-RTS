from enum import Enum, auto


class GridSquareTerrain(Enum):
    """
The terrain that each grid square can have.
    """

    CLEAR = auto()

    HILL = auto()
    MOUNTAIN = auto()
    SNOW = auto()
    RIVER = auto()
