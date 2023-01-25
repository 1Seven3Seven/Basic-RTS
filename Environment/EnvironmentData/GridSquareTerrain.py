from enum import Enum


class GridSquareTerrain(Enum):
    """
The terrain that each grid square can have.
    """

    # Additional attributes
    weight: int

    def __new__(cls, value: str, weight: int = 0) -> 'GridSquareTerrain':
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.weight = weight

        return obj

    CLEAR = ('Clear', 0)

    HILL = ('Hill', 6)
    MOUNTAIN = ('Mountain', 20)
    SNOW = ('Snow', 30)
    RIVER = ('River', 25)
