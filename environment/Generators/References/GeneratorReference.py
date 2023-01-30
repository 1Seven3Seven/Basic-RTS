from environment.Generators import BaseGenerator
from . import AttributeReference


class GeneratorReference:
    """
Contains information about the attributes of a generator, such as the data type and the range of values.
Has to be manually set up.
    """

    def __init__(self, generator: BaseGenerator):
        self.references: list[AttributeReference] = []
