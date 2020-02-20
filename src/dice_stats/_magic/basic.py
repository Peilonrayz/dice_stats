"""
Methods all classes should define.

Methods that are at the base of the class, but don't need to be defined
in base_dice.py. These are things like :code:`str`, :code:`repr` and
:code:`bool`.

These are magic methods that any class should define to make Pythonic
development easier.
"""

from __future__ import annotations

from .._types import ChancesValue
from .mapping import MappingDice


class BasicDice(MappingDice):
    """Basic magic methods mixin class."""

    def __repr__(self) -> str:
        """Repr format of Dice."""
        name = type(self).__qualname__
        values = {k: self[k] for k in sorted(self._chances)}
        return f"{name}[{self._total_chance}]({values!r})"

    def __str__(self) -> str:
        """Str format of Dice."""
        name = type(self).__qualname__
        keys = sorted(self._chances)
        max_k = len(str(max(keys)))
        sep = "\n  "
        value = sep.join(
            f"{k: >{max_k}}"
            f": {float(self[k]): >5.1%}"
            f" {self[k].numerator: >2}"
            f"/{self[k].denominator: <2}".rstrip()
            for k in keys
        )
        if not value:
            return f"{name}[{self._total_chance}]()"
        return f"{name}[{self._total_chance}]({sep}{value}\n)"

    def __bool__(self) -> bool:
        """Falsy if the only :ref:`ds-t-Chances Chance` is 0."""
        if self._total_chance == 0:
            return False
        if len(self._chances) != 1:
            return bool(self._chances)
        return 0 not in self._chances

    def __contains__(self, item: object) -> bool:
        """
        Is :ref:`ds-t-Chances Value` a possible :ref:`ds-t-Chances Chance`.

        This doesn't check if the :ref:`ds-t-Chances Value` is contained
        in the :ref:`ds-t-Internal Chances`. It checks if there is a
        potability of the dice. This is as some dice will show 0 as a
        :ref:`ds-t-Chances Value` with 0% :ref:`ds-t-Chances Chance`,
        however as it's not possible it doesn't make sense to say it's a
        :ref:`ds-t-Chances Chance` of the dice.
        """
        if not isinstance(item, ChancesValue):
            return False
        return bool(self._chances.get(item))
