from abc import ABC

from .. import NoiseMap, Environment


class BaseGenerator(ABC):
    """
A base class of an environment generator.
Used to generate specific aspects of the environment, e.g. terrain.
    """

    def __init__(self, environment: Environment):
        """
        :param environment: The environment the generator works on.
        """

        self.environment = environment

        self.noise_map: NoiseMap = NoiseMap(environment.x_size, environment.y_size)

    def generate_noise_map(self):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError
