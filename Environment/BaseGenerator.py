from abc import ABC

from . import NoiseMap
from .Environment import Environment


class BaseGenerator(ABC):
    def __init__(self, environment: Environment):
        """
A base class of an environment generator.
Used to generate specific aspects of the environment, e.g. terrain.
        :param environment: The environment the generator works on.
        """

        self.environment = environment

        self.noise_map: NoiseMap | None = None

    @property
    def noise_map(self) -> NoiseMap | None:
        if self.noise_map is None:
            return None

        return self.noise_map

    def generate_noise_map(self):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError
