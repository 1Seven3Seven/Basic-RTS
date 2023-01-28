from . import BaseGenerator


class GeneratorHandler:
    """
Holds multiple generator objects and handles the creation of the noise map and changing of the environment for them all.
    """

    def __init__(self, *args: BaseGenerator):
        """
Takes in any number of BaseGenerator children.
        """

        self.generators: list[BaseGenerator] = list(args)

    def generate_noise_maps(self):
        """
Gets all handled generators to create their noise maps.
        """

        for generator in self.generators:
            generator.generate_noise_map()

    def generate(self):
        """
Gets all handled generators to change the environment.
        """

        for generator in self.generators:
            generator.generate()
