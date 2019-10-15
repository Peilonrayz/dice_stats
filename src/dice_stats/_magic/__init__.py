"""
Magic methods for Dice class.

These add different types of magic methods to the dice class.
Given the amount of magic methods I found it to be clearer to split out
the definitions. This means numeric comparisons are located in the
numeric.py file.
"""

from .basic import BasicDice
from .numeric import NumericDice


class Dice(BasicDice, NumericDice):
    """Final Dice class with all magic methods."""
