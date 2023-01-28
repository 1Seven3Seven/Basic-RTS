"""
I do not know if this is a correct way of doing things, but as of writing this it works.
So here it is
"""

from environment import Generators

all_generators = Generators.__dict__.copy()
for key in list(all_generators.keys())[:]:
    if key.startswith('__'):  # Remove all dunders
        del all_generators[key]
# Remove the BaseGenerator
del all_generators['BaseGenerator']
# Should be left with only the generator classes
