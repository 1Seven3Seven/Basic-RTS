# Must come first
from .BaseGenerator import BaseGenerator

# The rest
from .TerrainGenerator import TerrainGenerator
from .TreeGenerator import TreeGenerator
from .StoneGenerator import StoneGenerator

# A dictionary containing all the generators
from ._all_generators import all_generators

# ToDo: Add in a generator handler that you pass multiply base generators, and it handles things for you.