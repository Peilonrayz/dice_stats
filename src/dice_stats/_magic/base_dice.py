"""
Core of the dice class.

These methods are the core of the dice class and the minimum needed for
the other mixins to extend from. These mostly focus on allowing the dice
to be initialized correctly.
"""

from __future__ import annotations

import copy
import fractions
from typing import Optional, cast

from .._types import TChances, TChancesChance, TChancesValue, TTotalChance


class BaseDice:
    """
    Base Dice class, defines standard methods for initializing dice objects.

    Other magic dice classes inherit from this.
    """

    __slots__ = ("_chances", "_total_chance")
    _chances: TChances
    _total_chance: TTotalChance

    def __init__(
        self,
        chances: Optional[TChances] = None,
        total_chance: TChancesChance = fractions.Fraction(1, 1),
    ) -> None:
        """
        Initialize Dice class.

        :param chances: :ref:`ds-t-Internal Chances` dictionary.
        :param total_chance: :ref:`ds-t-Total Chance` which allows a dice to
                             have a 50% chance, whilst allowing the
                             :ref:`ds-t-Internal Chances` to total 1.
        """
        if chances is None:
            chances = {}
        if any(
            not isinstance(value, fractions.Fraction) for value in chances.values()
        ):  # noqa
            raise TypeError("Damage contains values that aren't" " fractions.Fraction.")
        if not isinstance(total_chance, fractions.Fraction):
            raise TypeError("Chance isn't a fractions.Fraction.")
        if sum(chances.values()) != 1:
            raise ValueError(
                f"Chances don't add to 1, add to" f" {sum(chances.values())}."
            )

        self._chances = copy.deepcopy(chances)
        self._total_chance = total_chance

    def copy(self):
        """
        Create a copy of the current dice.

        This allows other methods to easily mutate a copy of a provided
        dice without mutating the dice a user provides. This helps keep
        the purity of a lot of the functions in this library.

        :return: A copy of this dice, including its type.
        """
        return type(self)(self._chances, total_chance=self.total_chance)

    @property
    def total_chance(self) -> TTotalChance:
        """
        :ref:`ds-t-Total Chance` of the values of this dice.

        :return: The :ref:`ds-t-Total Chance` of the dice.
        """
        return self._total_chance

    @classmethod
    def from_partial(  # pylint:disable=keyword-arg-before-vararg
        cls,
        chances: Optional[TChances] = None,
        total_chance: TTotalChance = fractions.Fraction(1, 1),
    ):
        """
        From partial :ref:`ds-t-Internal Chances`.

        This is a helper function to build dice from the
        :ref:`ds-t-Internal Chances`, where the chance's always
        total 1. By defaulting all undefined :ref:`ds-t-Chances Chance`
        to the chance of 0, rather than erroring.

        This may become deprecated in the future, as it seems like there
        is no use for this method.

        :param chances: :ref:`ds-t-Internal Chances` object.
        :param total_chance: :ref:`ds-t-Total Chance`.
        :return: A new dice with the provided chances.
        """
        chances = {} if chances is None else chances
        missing = 1 - sum(
            chances.values(),  # type: ignore
            fractions.Fraction(),  # type: ignore
        )
        default_key = cast(TChancesValue, 0)
        chances.setdefault(default_key, fractions.Fraction())
        chances[default_key] += missing
        return cls(chances, total_chance=total_chance)

    @classmethod
    def from_full(  # pylint:disable=keyword-arg-before-vararg
        cls, chances: TChances, total_chance: TTotalChance = fractions.Fraction(1, 1),
    ):
        """
        From full :ref:`ds-t-Internal Chances`.

        This is a helper function to build dice from the
        :ref:`ds-t-Internal Chances`.
        Allowing a different :ref:`ds-t-Total Chance`.

        :param chances: :ref:`ds-t-Internal Chances` object.
        :param total_chance: :ref:`ds-t-Total Chance`.
        :return: A new dice with the provided chances.
        """
        return cls(chances, total_chance=total_chance)

    @classmethod
    def from_empty(cls, value: TChancesValue = cast(TChancesValue, 0)):
        """
        Create an empty chance.

        A :ref:`ds-t-Chances Value` must be specified and so defaults to
        0 as the unwanted value.

        :param value: :ref:`ds-t-Chances Value` of the failure value.
        :return: An empty dice.
        """
        return cls(
            {value: fractions.Fraction(1, 1)}, total_chance=fractions.Fraction(1, 1),
        )
