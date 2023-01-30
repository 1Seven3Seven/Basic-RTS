# Must come first
from .BaseGenerator import BaseGenerator

# The generators next
from .TerrainGenerator import TerrainGenerator
from .TreeGenerator import TreeGenerator
from .StoneGenerator import StoneGenerator

# Then a dictionary containing all the generators
from ._all_generators import all_generators

# Finally a class to handle other generators
from .GeneratorHandler import GeneratorHandler

# Generator references
import References
