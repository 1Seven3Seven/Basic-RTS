# Must come first
from .BaseGenerator import BaseGenerator

# The rest
from .TerrainGenerator import TerrainGenerator
from .TreeGenerator import TreeGenerator
from .StoneGenerator import StoneGenerator

# ToDo: Add in a generator handler that you pass multiply base generators, and it handles things for you.