from environment.Generators import BaseGenerator
from . import AttributeReference


class GeneratorReference:
    """
Contains information about the attributes of a generator, such as the data type and the range of values.
Has to be manually set up.
    """

    def __init__(self, generator: BaseGenerator, *args: AttributeReference):
        self.generator: BaseGenerator = generator

        self.references: list[AttributeReference] = list(args)

    def check_all_references_are_valid(self):
        """
Raises an AttributeError if an AttributeReference.name isn't found in the generator dictionary.
        """

        for reference in self.references:
            if reference.name not in self.generator.__dict__:
                raise AttributeError(f"Attribute '{reference.name}' not found in {self.generator}")
