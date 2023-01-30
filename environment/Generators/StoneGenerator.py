from math import sqrt

from perlin_noise import PerlinNoise

from . import BaseGenerator
from .. import Environment
from ..EnvironmentData import GridSquareTerrain, GridSquareStructures


class StoneGenerator(BaseGenerator):
    """
Allows for the generation of stone deposits for the given environment.
    """

    def __init__(self,
                 environment: Environment,
                 seed: int = 1,
                 octaves: list[int] | None = None,
                 player_base_radius: int = 30,
                 clear_terrain_base_chance: float = -1.,
                 hill_terrain_base_chance: float = 0.,
                 mountain_terrain_base_chance: float = 0.15,
                 snow_terrain_base_chance: float = 0.25):
        """
Negative values for the base terrain chances means don't spawn stone deposits on that type of terrain.
        :param environment: The environment to generate stone deposits for.
        :param seed: The seed to use when using random numbers.
        :param octaves: The octaves to use when generating the noise map, in order of strength: 0.5 then 0.25 ...
        Default is [30, 60]
        :param player_base_radius: The radius around a base for which no stone deposits will spawn.
        :param clear_terrain_base_chance: The base chance for spawning trees on a clearing.
        :param hill_terrain_base_chance: The base chance for spawning trees on a hill.
        :param mountain_terrain_base_chance: The base chance for spawning trees on a mountain.
        :param snow_terrain_base_chance: The base chance for spawning trees on snow.
        """

        super().__init__(environment)

        self._seed: int = seed
        self._octaves: list[int] = octaves if octaves is not None else [30, 60]

        self._player_base_radius: int = player_base_radius

        self._clear_terrain_base_chance: float = clear_terrain_base_chance
        self._hill_terrain_base_chance: float = hill_terrain_base_chance
        self._mountain_terrain_base_chance: float = mountain_terrain_base_chance
        self._snow_terrain_base_chance: float = snow_terrain_base_chance

        self.sanity_check()

    # region - Getters
    @property
    def seed(self) -> int:
        return self._seed

    @property
    def octaves(self) -> list[int]:
        return self._octaves.copy()

    @property
    def player_base_radius(self) -> int:
        return self._player_base_radius

    @property
    def clear_terrain_base_chance(self) -> float:
        return self._clear_terrain_base_chance

    @property
    def hill_terrain_base_chance(self) -> float:
        return self._hill_terrain_base_chance

    @property
    def mountain_terrain_base_chance(self) -> float:
        return self._mountain_terrain_base_chance

    @property
    def snow_terrain_base_chance(self) -> float:
        return self._snow_terrain_base_chance

    # endregion - Getters

    # region - Setters
    @seed.setter
    def seed(self, new_seed: int):
        assert isinstance(new_seed, int), "Seed must be a positive integer"
        assert new_seed > 0, "Seed must be a positive integer"

        self._seed = new_seed
        self.make_out_of_date()

    @octaves.setter
    def octaves(self, new_octaves: list[int]):
        assert isinstance(new_octaves, list), "Octaves must be a list of positive integers"
        assert new_octaves, "Octaves must be a list of positive integers"
        assert [None for octave in new_octaves if octave > 0], "Octaves must be a list of positive integers"

        self._octaves = new_octaves.copy()
        self.make_out_of_date()

    @player_base_radius.setter
    def player_base_radius(self, new_radius: int):
        assert isinstance(new_radius, int), "Player base radius must be a positive integer"
        assert new_radius > 0, "Player base radius must be a positive integer"

        self._player_base_radius = new_radius
        self.make_out_of_date()

    @clear_terrain_base_chance.setter
    def clear_terrain_base_chance(self, new_chance: float):
        assert isinstance(new_chance, float), "Base clearing chance must be a float in the range (-inf, 1]"
        assert new_chance <= 1, "Base clearing chance must be a float in the range (-inf, 1]"

        self._clear_terrain_base_chance = new_chance
        self.make_out_of_date()

    @hill_terrain_base_chance.setter
    def hill_terrain_base_chance(self, new_chance: float):
        assert isinstance(new_chance, float), "Base hill chance must be a float in the range (-inf, 1]"
        assert new_chance <= 1, "Base hill chance must be a float in the range (-inf, 1]"

        self._hill_terrain_base_chance = new_chance
        self.make_out_of_date()

    @mountain_terrain_base_chance.setter
    def mountain_terrain_base_chance(self, new_chance: float):
        assert isinstance(new_chance, float), "Base mountain chance must be a float in the range (-inf, 1]"
        assert new_chance <= 1, "Base mountain chance must be a float in the range (-inf, 1]"

        self._mountain_terrain_base_chance = new_chance
        self.make_out_of_date()

    @snow_terrain_base_chance.setter
    def snow_terrain_base_chance(self, new_chance: float):
        assert isinstance(new_chance, float), "Base snow chance must be a float in the range (-inf, 1]"
        assert new_chance <= 1, "Base snow chance must be a float in the range (-inf, 1]"

        self._snow_terrain_base_chance = new_chance
        self.make_out_of_date()

    # endregion - Setters

    def sanity_check(self):
        """
A quick sanity check to see if all variables make sense.
Runs a bunch of asserts checking for correct values.
Honestly I think this is unnecessary.
        """

        self.save_out_of_date()

        self.seed = self._seed
        self.octaves = self._octaves
        self.player_base_radius = self._player_base_radius
        self.clear_terrain_base_chance = self._clear_terrain_base_chance
        self.hill_terrain_base_chance = self._hill_terrain_base_chance
        self.mountain_terrain_base_chance = self._mountain_terrain_base_chance
        self.snow_terrain_base_chance = self._snow_terrain_base_chance

        self.return_out_of_date()

    def generate_noise_map(self):
        """
Generates the noise map using the information stored.
Should be called after changing any values.
        """

        # Mr Clean 2
        self.noise_map.clear()

        # Add perlin noise
        all_noise = [PerlinNoise(octaves=octave, seed=self._seed) for octave in self._octaves]
        for y in range(self.environment.y_size):
            for x in range(self.environment.x_size):
                for i, noise in enumerate(all_noise, start=2):
                    self.noise_map[x, y] += noise([x / self.environment.x_size, y / self.environment.y_size]) / i

        self.noise_map.normalise_values()

        # Terrain base chances
        for y in range(self.environment.y_size):
            for x in range(self.environment.x_size):
                terrain = self.environment[x, y].terrain

                if terrain == GridSquareTerrain.CLEAR:
                    if self._clear_terrain_base_chance < 0:
                        self.noise_map[x, y] = float('-inf')
                    else:
                        self.noise_map[x, y] += self._clear_terrain_base_chance

                elif terrain == GridSquareTerrain.HILL:
                    if self._hill_terrain_base_chance < 0:
                        self.noise_map[x, y] = float('-inf')
                    else:
                        self.noise_map[x, y] += self._hill_terrain_base_chance

                elif terrain == GridSquareTerrain.MOUNTAIN:
                    if self._mountain_terrain_base_chance < 0:
                        self.noise_map[x, y] = float('-inf')
                    else:
                        self.noise_map[x, y] += self._mountain_terrain_base_chance

                elif terrain == GridSquareTerrain.SNOW:
                    if self._snow_terrain_base_chance < 0:
                        self.noise_map[x, y] = float('-inf')
                    else:
                        self.noise_map[x, y] += self._snow_terrain_base_chance

                # Remove close to bases
                for location in self.environment.player_base_locations:
                    distance = sqrt((location[0] - x) ** 2 + (location[1] - y) ** 2)

                    if distance < self._player_base_radius:
                        self.noise_map[x, y] = 0

        # In date
        self.make_in_date()

    def generate(self):
        """
Sets the structure parameter in grid squares if a random number is less than the noise value.
Ignores any grid squares that already have a structure.
        """

        assert self.is_out_of_date is False, "Current noise map is out of date, please call generate_noise_map before " \
                                            "this"

        for y in range(self.environment.y_size):
            for x in range(self.environment.x_size):
                if self.environment[x, y].terrain == GridSquareTerrain.RIVER:
                    continue

                if self.environment[x, y].structure != GridSquareStructures.NONE:
                    continue

                if self.noise_map[x, y] > 0.85:
                    self.environment[x, y].structure = GridSquareStructures.STONE
