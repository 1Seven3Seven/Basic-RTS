from math import sqrt

from perlin_noise import PerlinNoise

from . import BaseGenerator
from .. import Environment
from ..EnvironmentData import GridSquareTerrain


class TerrainGenerator(BaseGenerator):
    """
Allows for the generation of terrain for the given environment.
    """

    def __init__(self,
                 environment: Environment,
                 seed: int = 1,
                 octaves: list[int] | None = None,
                 snow_height: float = 0.9,
                 mountain_height: float = 0.75,
                 hill_height: float = 0.5):
        """
Separated from the environment code because it got too messy.
        :param environment: The environment to generate the terrain for.
        :param seed: The seed to use when using random numbers. Same seed -> same result.
        :param octaves: The octaves to use when generating the noise map, in order of strength: 0.5 then 0.25 ... Default is [3, 6, 12, 24]
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

        self.sanity_check()

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

    @snow_height.setter
    def snow_height(self, new_snow_height: float):
        assert isinstance(new_snow_height, float), "Snow height must be a float between 0 and 1"
        assert 0 < new_snow_height < 1, "Snow height must be a float between 0 and 1"

        self._snow_height = new_snow_height
        self.make_out_of_date()

    @mountain_height.setter
    def mountain_height(self, new_mountain_height: float):
        assert isinstance(new_mountain_height, float), "Mountain height must be a float between 0 and 1 and less " \
                                                       "than snow height"
        assert 0 < new_mountain_height < 1, "Mountain height must be a float between 0 and 1 and less than snow height"
        assert new_mountain_height < self._snow_height, "Mountain height must be a float between 0 and 1 and less " \
                                                        "than snow height"

        self._mountain_height = new_mountain_height
        self.make_out_of_date()

    @hill_height.setter
    def hill_height(self, new_hill_height: float):
        assert isinstance(new_hill_height, float), "Hill height must be a float between 0 and 1 and less than " \
                                                   "mountain height"
        assert 0 < new_hill_height < 1, "Hill height must be a float between 0 and 1 and less than mountain height"
        assert new_hill_height < self._mountain_height, "Hill height must be a float between 0 and 1 and less than " \
                                                        "mountain height"

        self._hill_height = new_hill_height
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
        self.snow_height = self._snow_height
        self.mountain_height = self._mountain_height
        self.hill_height = self._hill_height

        self.return_out_of_date()

    def generate_noise_map(self):
        """
Generates the noise map using the information stored.
Should be called after changing any values.
        """

        all_noise = [PerlinNoise(octaves=octave, seed=self._seed) for octave in self._octaves]

        center_x, center_y = self.environment.x_size / 2, self.environment.y_size / 2

        largest_value = sqrt(center_x * center_x + center_y * center_y)

        self.noise_map.clear()

        for y in range(self.environment.y_size):
            for x in range(self.environment.x_size):
                value = largest_value - sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                value /= largest_value

                for i, noise in enumerate(all_noise, start=2):
                    value += noise([x / self.environment.x_size, y / self.environment.y_size]) / i

                self.noise_map[x, y] = value

        # Normalise
        self.noise_map.normalise_values()

        # Now in date
        self.make_in_date()

    def generate(self):
        """
Sets the terrain parameter in every grid square of the environment according to the noise map.
        """

        assert self.is_out_of_date is False, "Current noise map is out of date, please call generate_noise_map before " \
                                             "this"

        for y in range(self.environment.y_size):
            for x in range(self.environment.x_size):
                value = self.noise_map[x, y]

                terrain_type = GridSquareTerrain.CLEAR
                if value > self._snow_height:
                    terrain_type = GridSquareTerrain.SNOW
                elif value > self._mountain_height:
                    terrain_type = GridSquareTerrain.MOUNTAIN
                elif value > self._hill_height:
                    terrain_type = GridSquareTerrain.HILL

                self.environment[x, y].terrain = terrain_type
