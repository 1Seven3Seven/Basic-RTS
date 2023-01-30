from . import BaseGenerator


class GeneratorHandler:
    """
Holds multiple generator objects and handles the creation of the noise map and changing of the environment for them all.
    """

    def __init__(self, *args: BaseGenerator):
        """
Takes in any number of BaseGenerator children.
Generators that change terrain should come first so ones that use the terrain can work correctly.
        """

        self.generators: list[BaseGenerator] = list(args)

    def generate(self):
        """
Runs through every generator provided and if the noise map is out of date, generates it, otherwise just changes  the environment.
        """

        for generator in self.generators:
            if generator.is_out_of_date:
                generator.generate_noise_map()

            generator.generate()
