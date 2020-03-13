"""
Numeric operators.

Add support for using Dice numerically. For the most part all operations
should work as expected. But two methods have two different ways they
could be reasonably expected to work.

For the examples :code:`d6` is defined as :code:`Dice.from_dice(6)`.

 - Most operations work as if you were applying that function to all
   values in the dice. This means if you were to use
   :code:`Dice.from_dice(6) + 2` then the values would range from 3 to 8,
   rather than from 1 to 6. The chance for all would still be 1/6.

   You can also add dice to other dice. :code:`d6 + d6` would result in
   a triangle chance with 7 being the most likely result.

 - However it is unclear what :code:`2 * d6` should result in. This is
   as 2d6 is a common way to denote rolling two d6s and adding the
   results together. Which is the same as :code:`d6 + d6`.

   There is then the option of performing the cartesian product of
   :code:`{2}` and :code:`{1, 2, 3, 4, 5, 6}`, which would result in
   :code:`{2, 4, 6, 8, 10, 12}`.

   Given that both make sense, but we can only define one to be _the_
   multiplication operator. We have decided to keep with common
   convention and have made the multiplication operator work the same
   way as :code:`d6 + d6`. If the cartesian product is required then it
   is available via the :code:`non_repeat` property. Such as
   :code:`2 * d6.non_repeat`.

   We have also changed the power operator to work in the same way.
   And so :code:`d6 ** 2` is the same as :code:`d6 * d6.non_repeat`.
"""

from __future__ import annotations

import collections
import fractions
import functools
import operator
from typing import Callable, Optional, Union, cast

from .._types import ChancesValue, TChancesDD, TChancesValue, TIntNumber
from .mapping import MappingDice

# TODO: __divmod__
Other = Union[MappingDice, TChancesValue]


class NumericDice(MappingDice):
    """Mixins for numeric operators."""

    def __add__(self, other: Other,) -> NumericDice:
        return operation(self, other, operator.add)

    def __radd__(self, other: Other,) -> NumericDice:
        return roperation(other, self, operator.add)

    def __sub__(self, other: Other,) -> NumericDice:
        return operation(self, other, operator.sub)

    def __rsub__(self, other: Other,) -> NumericDice:
        return roperation(other, self, operator.sub)

    def __truediv__(self, other: Other,) -> NumericDice:
        return operation(self, other, operator.truediv)

    def __rtruediv__(self, other: Other,) -> NumericDice:
        return roperation(other, self, operator.truediv)

    def __floordiv__(self, other: Other,) -> NumericDice:
        return operation(self, other, operator.floordiv)

    def __rfloordiv__(self, other: Other,) -> NumericDice:
        return roperation(other, self, operator.floordiv)

    def __mod__(self, other: Other,) -> NumericDice:
        return operation(self, other, operator.mod)

    def __rmod__(self, other: Other,) -> NumericDice:
        return roperation(other, self, operator.mod)

    def __lshift__(self, other: Other,) -> NumericDice:
        return operation(self, other, operator.lshift)

    def __rlshift__(self, other: Other,) -> NumericDice:
        return roperation(other, self, operator.lshift)

    def __rshift__(self, other: Other,) -> NumericDice:
        return operation(self, other, operator.rshift)

    def __rrshift__(self, other: Other,) -> NumericDice:
        return roperation(other, self, operator.rshift)

    def __and__(self, other: Other,) -> NumericDice:
        return operation(self, other, operator.and_)

    def __rand__(self, other: Other,) -> NumericDice:
        return roperation(other, self, operator.and_)

    def __xor__(self, other: Other,) -> NumericDice:
        return operation(self, other, operator.xor)

    def __rxor__(self, other: Other,) -> NumericDice:
        return roperation(other, self, operator.xor)

    def __or__(self, other: Other,) -> NumericDice:
        return operation(self, other, operator.or_)

    def __ror__(self, other: Other,) -> NumericDice:
        return roperation(other, self, operator.or_)

    def __neg__(self) -> NumericDice:
        return soperation(self, operator.neg)

    def __pos__(self) -> NumericDice:
        return soperation(self, operator.pos)

    def __abs__(self) -> NumericDice:
        return soperation(self, operator.abs)

    def __invert__(self) -> NumericDice:
        return soperation(self, operator.invert)

    # Special

    def __mul__(self, other: TIntNumber) -> NumericDice:
        return repeat_operation(self, other, operator.add)

    def __rmul__(self, other: TIntNumber) -> NumericDice:
        return repeat_operation(self, other, operator.add)

    def __pow__(self, other: TIntNumber) -> NumericDice:
        return repeat_operation(self, other, operator.pow)

    def __rpow__(self, other: TIntNumber) -> NumericDice:
        return repeat_operation(self, other, operator.pow)

    @property
    def non_repeat(self) -> NonRepeat:
        """Build a NonRepeat object."""
        return NonRepeat(self)


def repeat_operation(
    dice: NumericDice,
    value: TIntNumber,
    operator_: Callable[[NumericDice, NumericDice], NumericDice],
) -> NumericDice:
    """Handle repeating an operation."""
    if not isinstance(value, TIntNumber):
        raise TypeError("Non-dice operand must be a number.")
    if value == 0:
        return type(dice).from_partial(total_chance=dice.total_chance)
    if value < 0:
        raise ValueError("Power must be non-negative.")
    if value % 1:
        raise ValueError("Power must be an integer.")
    new_dice = dice.copy()
    for _ in range(value - 1):
        new_dice = operator_(new_dice, dice)
    return new_dice


# pylint:disable=protected-access
def operation(
    lhs: MappingDice,
    rhs: object,
    operation_: Callable[[TChancesValue, TChancesValue], TChancesValue],
) -> NumericDice:
    """Handle the normal direction of operations."""
    new: TChancesDD = collections.defaultdict(fractions.Fraction)
    if isinstance(rhs, MappingDice):
        if lhs.total_chance != rhs.total_chance:
            raise ValueError("Can't multiply two dice with different total chances")
        for value_1, chance_1 in lhs._chances.items():
            for value_2, chance_2 in rhs._chances.items():
                new[operation_(value_1, value_2)] += chance_1 * chance_2
        return type(lhs).from_full(new, total_chance=lhs.total_chance)

    if isinstance(rhs, ChancesValue):
        for value, chance in lhs._chances.items():
            new[operation_(value, rhs)] += chance
        return type(lhs).from_full(new, total_chance=lhs.total_chance)

    return NotImplemented


def roperation(
    lhs: object,
    rhs: MappingDice,
    operator_: Callable[[TChancesValue, TChancesValue], TChancesValue],
) -> NumericDice:
    """Handle the reverse of common operations."""
    new: TChancesDD = collections.defaultdict(fractions.Fraction)
    if isinstance(lhs, MappingDice):
        for value_1, chance_1 in rhs._chances.items():
            for value_2, chance_2 in lhs._chances.items():
                new[operator_(value_2, value_1)] += chance_1 * chance_2
        return type(rhs).from_full(
            new, total_chance=lhs.total_chance * rhs.total_chance
        )

    if isinstance(lhs, ChancesValue):
        for value, chance in rhs._chances.items():
            new[operator_(value, lhs)] += chance
        return type(rhs).from_full(new, total_chance=rhs.total_chance)

    return NotImplemented


def soperation(
    self: MappingDice, operator_: Callable[[TChancesValue], TChancesValue]
) -> NumericDice:
    """Handel's single operand operations."""
    new: TChancesDD = collections.defaultdict(fractions.Fraction)
    for value, chance in self.items():
        new[operator_(value)] += chance
    return type(self).from_full(new, total_chance=self.total_chance)


class NonRepeat:
    """Allow alternate form of multiplication and powers."""

    __slots__ = ("_dice",)
    _dice: MappingDice

    def __init__(self, dice: NumericDice) -> None:
        """Initialize NonRepeat class."""
        self._dice = dice

    def __mul__(self, other: Other) -> NumericDice:
        return operation(self._dice, other, operator.mul)

    def __rmul__(self, other: Other) -> NumericDice:
        return roperation(other, self._dice, operator.mul)

    def __pow__(
        self, other: Other, modulo: Optional[TChancesValue] = None,
    ) -> NumericDice:
        return operation(
            self._dice,
            other,
            cast(
                Callable[[TChancesValue, TChancesValue], TChancesValue],
                operator.pow
                if modulo is None
                else functools.partial(operator.pow, modulo=modulo),
            ),
        )

    def __rpow__(
        self, other: Other, modulo: Optional[TChancesValue] = None
    ) -> NumericDice:
        return roperation(
            other,
            self._dice,
            cast(
                Callable[[TChancesValue, TChancesValue], TChancesValue],
                operator.pow
                if modulo is None
                else functools.partial(operator.pow, modulo=modulo),
            ),
        )
