import math


class NoiseMap:
    def __init__(self, x_size: int, y_size: int):
        self._x_size: int = x_size
        self._y_size: int = y_size

        self._noise_map: list[list[float]] = [[0 for _ in range(x_size)] for _ in range(y_size)]

    def __getitem__(self, coords: tuple[int, int]) -> float:
        """
Returns the noise value at the given coordinates.
Raises an IndexError of the coords are out of bounds.
Does not work with slices.
        :param coords: The coordinates of the noise to lookup.
        :return: The noise at the coordinates.
        """

        x, y = coords

        assert isinstance(x, int) and isinstance(y, int), "Coordinates need to be integers"

        # Check for within bounds
        if x < 0 or x >= self._x_size:
            raise IndexError(f"Provided x coordinate '{x}' is not within the bounds [0, {self._x_size})")
        if y < 0 or y >= self._y_size:
            raise IndexError(f"Provided y coordinate '{y}' is not within the bounds [0, {self._y_size})")

        return self._noise_map[y][x]

    def __setitem__(self, coords: tuple[int, int], value: float) -> None:
        """
Sets the value of the noise at the given coordinates.
Raises an IndexError of the coords are out of bounds.
        :param coords:The coordinates of the noise to set.
        :param value: The value to set the noise to.
        """

        x, y = coords

        assert isinstance(x, int) and isinstance(y, int), "Coordinates need to be integers"

        # Check for within bounds
        if x < 0 or x >= self._x_size:
            raise IndexError(f"Provided x coordinate '{x}' is not within the bounds [0, {self._x_size})")
        if y < 0 or y >= self._y_size:
            raise IndexError(f"Provided y coordinate '{y}' is not within the bounds [0, {self._y_size})")

        self._noise_map[y][x] = value

    # region - Getters
    @property
    def x_size(self) -> int:
        return self._x_size

    @property
    def y_size(self) -> int:
        return self._y_size

    # endregion - Getters

    def clear(self) -> None:
        """
Returns all values in the noise map to 0.
        """

        self._noise_map: list[list[float]] = [[0 for _ in range(self._x_size)] for _ in range(self._y_size)]

    def normalise_values(self) -> None:
        """
Forces every value to be between 0 and 1, inclusive.
        """

        abs_min_value = abs(min([min([value for value in row if not math.isinf(value)]) for row in self._noise_map]))
        self._noise_map = [[value + abs_min_value for value in row] for row in self._noise_map]

        max_value = max([max([value for value in row if not math.isinf(value)]) for row in self._noise_map])
        self._noise_map = [[value / max_value for value in row] for row in self._noise_map]
