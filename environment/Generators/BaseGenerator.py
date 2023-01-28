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
        
        self._out_of_date: bool = True
        self._out_of_date_save: bool = True
    
    @property
    def is_out_of_date(self):
        return self._out_of_date
        
    def make_out_of_date(self):
        self._out_of_date = True
        
    def make_in_date(self):
        self._out_of_date = False
        
    def save_out_of_date(self):
        self._out_of_date_save = self._out_of_date
        
    def return_out_of_date(self):
        self._out_of_date = self._out_of_date_save

    def generate_noise_map(self):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError
