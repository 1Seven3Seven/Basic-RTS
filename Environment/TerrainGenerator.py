from copy import copy
from math import sqrt

from perlin_noise import PerlinNoise

from . import BaseGenerator, NoiseMap
from . import Environment
from .EnvironmentData import GridSquareTerrain


class TerrainGenerator(BaseGenerator):
    def __init__(self,
                 environment: Environment,
                 seed: int = 1,
                 octaves: list[int] | None = None,
                 snow_height: float = 0.9,
                 mountain_height: float = 0.75,
                 hill_height: float = 0.5):
        """
Allows for the generation of terrain for the given environment.
Separated from the environment code because it got too messy.
        :param environment: The environment to generate the terrain for.
        :param seed: The seed to use when using random numbers. Same seed -> same result.
        :param octaves: The octaves to use when generating the noise map, in order of strength: 0.5 then 0.25 ...
        :param snow_height: The minimum height for snow.
        :param mountain_height: The minimum height for mountain, must be less than snow height.
        :param hill_height: The minimum height for hill, must be less than mountain height.
        """

        super().__init__(environment)

        self._seed: int = seed
        self._octaves: list[int] = octaves if octaves is not None else [3, 6, 12, 24]
        self._snow_height: float = snow_height
        self._mountain_height: float = mountain_height
        self._hill_height: float = hill_height

        # If the parameters have been changed and the noise map hasn't been regenerated
        self.__out_of_date: bool = True

        self.sanity_check()

        self._noise_map: NoiseMap = NoiseMap(environment.x_size, environment.y_size)

    # region - Getters
    @property
    def seed(self) -> int:
        return self._seed

    @property
    def octaves(self) -> list[int]:
        return self._octaves.copy()

    @property
    def snow_height(self) -> float:
        return self._snow_height

    @property
    def mountain_height(self) -> float:
        return self._mountain_height

    @property
    def hill_height(self) -> float:
        return self._hill_height

    @property
    def noise_map(self) -> NoiseMap:
        return copy(self._noise_map)

    # endregion - Getters

    # region - Setters
    @seed.setter
    def seed(self, new_seed: int):
        assert isinstance(new_seed, int), "Seed must be a positive integer"
        assert new_seed > 0, "Seed must be a positive integer"

        self._seed = new_seed
        self.__out_of_date = True

    @octaves.setter
    def octaves(self, new_octaves: list[int]):
        assert isinstance(new_octaves, list), "Octaves must be a list of positive integers"
        assert new_octaves, "Octaves must be a list of positive integers"
        assert [None for octave in new_octaves if octave > 0], "Octaves must be a list of positive integers"

        self._octaves = new_octaves.copy()
        self.__out_of_date = True

    @snow_height.setter
    def snow_height(self, new_snow_height: float):
        assert isinstance(new_snow_height, float), "Snow height must be a float between 0 and 1"
        assert 0 < new_snow_height < 1, "Snow height must be a float between 0 and 1"

        self._snow_height = new_snow_height
        self.__out_of_date = True

    @mountain_height.setter
    def mountain_height(self, new_mountain_height: float):
        assert isinstance(new_mountain_height, float), "Mountain height must be a float between 0 and 1 and less " \
                                                       "than snow height"
        assert 0 < new_mountain_height < 1, "Mountain height must be a float between 0 and 1 and less than snow height"
        assert new_mountain_height < self._snow_height, "Mountain height must be a float between 0 and 1 and less " \
                                                        "than snow height"

        self._mountain_height = new_mountain_height
        self.__out_of_date = True

    @hill_height.setter
    def hill_height(self, new_hill_height: float):
        assert isinstance(new_hill_height, float), "Hill height must be a float between 0 and 1 and less than " \
                                                   "mountain height"
        assert 0 < new_hill_height < 1, "Hill height must be a float between 0 and 1 and less than mountain height"
        assert new_hill_height < self._mountain_height, "Hill height must be a float between 0 and 1 and less than " \
                                                        "mountain height"

        self._hill_height = new_hill_height
        self.__out_of_date = True

    # endregion - Setters

    def sanity_check(self):
        """
A quick sanity check to see if all variables make sense.
Runs a bunch of asserts checking for correct values.
Honestly I think this is unnecessary.
        """

        out_of_date_save = self.__out_of_date

        self.seed = self._seed
        self.octaves = self._octaves
        self.snow_height = self._snow_height
        self.mountain_height = self._mountain_height
        self.hill_height = self._hill_height

        self.__out_of_date = out_of_date_save

    def generate_noise_map(self):
        """
Generates the noise map using the information given upon initialisation.
Should be called after changing any values.
        """

        all_noise = [PerlinNoise(octaves=octave, seed=self._seed) for octave in self._octaves]

        center_x, center_y = self.environment.x_size / 2, self.environment.y_size / 2

        largest_value = sqrt(center_x * center_x + center_y * center_y)

        self._noise_map.clear()
        
        for y in range(self.environment.y_size):
            for x in range(self.environment.x_size):
                value = largest_value - sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                value /= largest_value

                for i, noise in enumerate(all_noise, start=2):
                    value += noise([x / self.environment.x_size, y / self.environment.y_size])

                self._noise_map[x, y] = value

        # Normalise
        self._noise_map.normalise_values()

        # Now in date
        self.__out_of_date = False

    def generate(self):
        """
Sets the terrain parameter in every grid square of the environment according to the noise map.
        """

        assert self._noise_map is not None, "Noise map not generated, please call generate_noise_map before this"
        assert self.__out_of_date, "Current noise map is out of date, please call generate_noise_map before this"

        for y in range(self.environment.y_size):
            for x in range(self.environment.x_size):
                value = self._noise_map[x, y]

                terrain_type = GridSquareTerrain.CLEAR
                if value > self._snow_height:
                    terrain_type = GridSquareTerrain.SNOW
                elif value > self._mountain_height:
                    terrain_type = GridSquareTerrain.MOUNTAIN
                elif value > self._hill_height:
                    terrain_type = GridSquareTerrain.HILL

                self.environment[x, y].terrain = terrain_type
