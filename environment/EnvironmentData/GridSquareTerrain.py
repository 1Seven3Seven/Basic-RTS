from enum import Enum


class GridSquareTerrain(Enum):
    """
The terrain that each grid square can have.
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

    CLEAR = 0

    HILL = 6
    MOUNTAIN = 20
    SNOW = 30
    RIVER = 25
