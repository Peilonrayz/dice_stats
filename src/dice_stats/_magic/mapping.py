"""
Mapping interface.

Code to make Dice implement an immutable mapping interface.
This interface helps to keep code that uses dice Pythonic as they can
use standard methods, and it the immutability helps make all the code
simpler to use as we don't need to think about mutability.
"""

from __future__ import annotations

from typing import Iterator, Mapping
import fractions

from .base_dice import BaseDice
from .._types import TChancesValue, TChancesChance


class MappingDice(BaseDice, Mapping[TChancesValue, TChancesChance]):
    """Mapping mixin."""

    def __getitem__(self, item: TChancesValue) -> fractions.Fraction:
        """Get :ref:`ds-t-Chances Chance`."""
        return self._chances.__getitem__(item) * self._total_chance

    def __iter__(self) -> Iterator[TChancesValue]:
        """Get all :ref:`ds-t-Chances Value`."""
        return self._chances.__iter__()

    def __len__(self) -> int:
        """Count of all :ref:`ds-t-Chances Value`."""
        return self._chances.__len__()
