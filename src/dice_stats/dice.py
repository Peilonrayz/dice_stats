"""High level dice helper functions."""

from __future__ import annotations

import collections
import fractions
from typing import (
    Any, Callable, Dict, Iterable, Iterator, Optional, Set,
    Tuple, TypeVar, cast
)

from ._magic import Dice as BaseDice
from ._types import (
    TIntNumber, TChances, TChancesDD, TChancesValue, TTotalChance
)

T = TypeVar('T')  # pylint:disable=invalid-name


class Dice(BaseDice):
    """Dice class."""

    @classmethod
    def sum(cls, dice: Iterable[Dice]) -> Dice:
        """
        Add multiple dice together, increasing their :ref:`ds-t-Total Chance`.

        This is mostly used when you have multiple partial dice that you
        need to add together only adding the chances together. For
        example lets say we have a 2/3 chance for our outcome to be a d6
        or a 1/3 chance that the outcome is a d4 then the total outcome
        would be the result of those two dice added together, but not in
        the common form - :code:`d6 + d4`.

        .. testcode::

            print(Dice.sum([
                Dice.from_dice(6, total_chance=Fraction(2, 3)),
                Dice.from_dice(4, total_chance=Fraction(1, 3)),
            ]))

        Which correctly results in:

        .. testoutput::

            Dice[1](
              1: 19.4%  7/36
              2: 19.4%  7/36
              3: 19.4%  7/36
              4: 19.4%  7/36
              5: 11.1%  1/9
              6: 11.1%  1/9
            )

        As we can see, the result totals to 100%, and there is a
        significantly higher chance to get a 1-4 then 5 or 6.
        This shows pretty clearly that the outcome is only adding the
        chances together.

        For the most part you can normally use a different function than
        this one if you need to get this sort of output.
        Lets say the game we're playing says to roll a d3 to decide
        between either the d4 or the d6 to be rolled to get the result.
        On a 1 you roll the d4 otherwise it's the d6, which could be
        expressed as:

        .. testcode::

            print(
                Dice.from_dice(3)
                    .apply_dice(
                        {(1,): Dice.from_dice(4)},
                        Dice.from_dice(6)
                    )
            )

        .. testoutput::

            Dice[1](
              1: 19.4%  7/36
              2: 19.4%  7/36
              3: 19.4%  7/36
              4: 19.4%  7/36
              5: 11.1%  1/9
              6: 11.1%  1/9
            )
        """
        chances: TChancesDD = collections.defaultdict(fractions.Fraction)
        tot_chance = fractions.Fraction(0, 1)
        for die in dice:
            tot_chance += die.total_chance
            for amount, chance in die.items():
                chances[amount] += chance
        return cls.from_external(chances, total_chance=tot_chance)

    @classmethod
    def from_external(
            cls,
            chances: TChances,
            total_chance: TTotalChance
    ) -> Dice:
        """
        Create a dice from the :ref:`ds-t-Chances` form.

        This doesn't use the :ref:`ds-t-Internal Chances` form,
        and so eases use when not using that form.

        :param chances: :ref:`ds-t-Chances`.
        :param total_chance: :ref:`ds-t-Total Chance`.
        :return: A dice with the specified chances.
        """
        return cls.from_full(
            {
                value: chance / total_chance
                for value, chance in chances.items()
            },
            total_chance=total_chance
        )

    @classmethod
    def from_dice(
            cls,
            sides: TIntNumber,
            total_chance: TTotalChance = fractions.Fraction(1, 1),
    ) -> Dice:
        """
        Make a dice from a number of sides.

        This is a very useful convenience function, this is the most
        common way to build dice as it builds dice with an equal chance
        to land on all faces.

        :param sides: Amount of sides the n-sided dice has.
        :param total_chance: :ref:`ds-t-Total Chance`.
        :return: A fair n-sided dice.

        Below is an example of some of the smaller dice you can create
        with this.

        .. testcode::

            print(Dice.from_dice(1))
            print(Dice.from_dice(2))
            print(Dice.from_dice(3))
            print(Dice.from_dice(6))

        .. testoutput::

            Dice[1](
              1: 100.0%  1/1
            )
            Dice[1](
              1: 50.0%  1/2
              2: 50.0%  1/2
            )
            Dice[1](
              1: 33.3%  1/3
              2: 33.3%  1/3
              3: 33.3%  1/3
            )
            Dice[1](
              1: 16.7%  1/6
              2: 16.7%  1/6
              3: 16.7%  1/6
              4: 16.7%  1/6
              5: 16.7%  1/6
              6: 16.7%  1/6
            )
        """
        value = fractions.Fraction(1, cast(int, sides))
        values = {
            cast(TChancesValue, key): value
            for key in range(1, sides + 1)
        }
        return cls.from_full(values, total_chance=total_chance)

    @classmethod
    def from_prev_total_chance(
            cls,
            chances: TChances,
            chance: TTotalChance,
            prev_chance: TTotalChance,
    ) -> Dice:
        """
        Change a dice from one :ref:`ds-t-Total Chance` to another.

        This is a deprecated function, this is likely better expressed
        by using :meth:`dice_stats.Dice.from_external` and
        :meth:`dice_stats.Dice.as_total_chance`.

        :param chances: :ref:`ds-t-Chances`.
        :param chance: New :ref:`ds-t-Total Chance` amount.
        :param prev_chance: Old :ref:`ds-t-Total Chance` amount.
        :return: A dice with new chances.
        """
        delta = prev_chance / chance
        return cls.from_full(
            {
                key: value * delta
                for key, value in chances.items()
            },
            total_chance=chance,
        )

    def as_total_chance(self, total_chance: fractions.Fraction) -> Dice:
        """
        Change :ref:`ds-t-Total Chance`.

        This adjusts each :ref:`ds-t-Chances Chance` by the scale of
        the old and new :ref:`ds-t-Total Chance`.

        :param total_chance: Desired :ref:`ds-t-Total Chance`.
        :return: A new dice with the specified :ref:`ds-t-Total Chance`.

        For example, say we have a d3 which has a
        100% :ref:`ds-t-Total Chance`, however it should be a
        200% :ref:`ds-t-Total Chance`. Then we use this function to
        change it. It will also change all the :ref:`ds-t-Chances Chance`
        from 1/3 to 2/3.

        .. testcode::

            d3 = Dice.from_dice(3)
            print(d3)
            print(d3.as_total_chance(Fraction(2, 1)))

        .. testoutput::

            Dice[1](
              1: 33.3%  1/3
              2: 33.3%  1/3
              3: 33.3%  1/3
            )
            Dice[2](
              1: 66.7%  2/3
              2: 66.7%  2/3
              3: 66.7%  2/3
            )
        """
        return type(self)(self._chances, total_chance=total_chance)

    def apply_dice(
            self,
            chances: Dict[Iterable[TChancesValue], Dice],
            default: Optional[Dice] = None
    ) -> Dice:
        """
        Change chances to provided dice.

        This changes the values of the host dice, to the values of the
        provided dice. It does so by changing the provided dice to the
        correct chance.

        :param chances: A mapping of all the :ref:`ds-t-Chances Value`
                        and dice to change.
        :param default: A dice to use as the default when chances
                        doesn't cover all possible :ref:`ds-t-Chances Value`.
        :return: A new Dice that acts as if these multiple dice rolls
                 happen in one throw.

        Say we're playing a game where you roll a die to attack people.
        You normally do 1-6 damage, however sometimes there's a chance
        to do 1-4 - say you had bad footing. To determine what dice you
        use use throw a d3 before using either the d6 or the d4. On a 1
        you use the d4, otherwise it's the d6.
        To find the chances is easy with this function.

        .. testcode::

            print(
                Dice.from_dice(3)
                    .apply_dice(
                        {(1,): Dice.from_dice(4)},
                        Dice.from_dice(6),
                    )
            )

        .. testoutput::

            Dice[1](
              1: 19.4%  7/36
              2: 19.4%  7/36
              3: 19.4%  7/36
              4: 19.4%  7/36
              5: 11.1%  1/9
              6: 11.1%  1/9
            )
        """
        _chances_default(self, chances, default)
        return self.sum(
            dice.as_total_chance(chance)
            for _, chance, dice in _chances(self, chances)
        )

    # TODO: change to make the example not work, as it should change the %.
    def apply_functions(
            self,
            chances: Dict[Iterable[TChancesValue], Callable[[Dice], Dice]],
            default: Optional[Callable[[Dice], Dice]] = None,
            apply: Callable[[Dice], Dice] = lambda dice: dice,
    ) -> Dice:
        """
        Apply a callback to the provided chances.

        This is the more complex version :meth:`dice_stats.Dice.apply_dice`.
        With this version you can pass a callback that mutates the
        segment of the dice provided.

        This callback is given a segment of the host dice, this means
        that the callback has all the information that it should need,
        as this dice would have all the :ref:`ds-t-Chances Value` and
        :ref:`ds-t-Chances Chance` it needs. The :ref:`ds-t-Total Chance`
        will also be the correct for that segment of the dice results.

        The callback then has to return a dice object that that segment
        gets mutated to. For example if you're using this to reroll dice,
        then one function would return the segment provided, where the
        other would return the host dice of sorts.

        :param chances: The mapping that holds the outputs.
        :param default: The function to apply if there are missing values.
        :param apply: A function to mutate each dice segment before they
                      reach the :code:`chances` callback.
        :return: New dice that's been fully mutated by the callbacks.

        To expand on the previous example, if we have a d6 and we're
        allowed to reroll 1s once, then we could use the following code.

        .. note::

            This functionality is already builtin to the
            :class:`dice_stats.Dice` class. You can instead use the
            :meth:`dice_stats.Dice.reroll` method to do this.

        .. testcode::

            print(
                Dice.from_dice(6)
                    .apply_functions(
                        {(1,): lambda _: Dice.from_dice(6)},
                        lambda d: d,
                    )
            )

        .. testoutput::

            Dice[1](
              1:  2.8%  1/36
              2: 19.4%  7/36
              3: 19.4%  7/36
              4: 19.4%  7/36
              5: 19.4%  7/36
              6: 19.4%  7/36
            )
        """
        _chances_default(self, chances, default)
        return self.sum(
            dice.as_total_chance(chance)
            for _, chance, dice in _apply_chances(self, chances, apply)
        )

    def partition(self, values: Iterable[TChancesValue]) -> Tuple[Dice, Dice]:
        """
        Remove multiple :ref:`ds-t-Chances Value` from the dice.

        Split the dice into two. This removes the values provided in
        the values argument out of the dice, and then returns the rest
        of the values in a separate dice.

        :param values: Selection of :ref:`ds-t-Chances Value` to remove
                       from the dice.
        :return: Returns two different dice, one with the wanted values,
                 the other with the unwanted values.

        For the most part this is used internally when using one of the
        apply functions or the reroll function. However its existence
        helps makes these functions possible and easy to implement.

        To showcase this we'll define a basic reroll function using this
        function.

        .. note::

            This functionality is already builtin to the
            :class:`dice_stats.Dice` class. You can instead use the
            :meth:`dice_stats.Dice.reroll` method to do this.

        .. testcode::

            def reroll(dice, values):
                rerolled, kept = dice.partition(values)
                return Dice.sum([
                    kept,
                    dice.as_total_chance(rerolled.total_chance),
                ])

            print(reroll(Dice.from_dice(6), (1,)))

        .. testoutput::

            Dice[1](
              1:  2.8%  1/36
              2: 19.4%  7/36
              3: 19.4%  7/36
              4: 19.4%  7/36
              5: 19.4%  7/36
              6: 19.4%  7/36
            )
        """
        one = fractions.Fraction(1, 1)
        dice_values = self._chances.copy()
        chances: TChances = {
            value: dice_values.pop(value)
            for value in values
        }
        chance = sum(chances.values(), fractions.Fraction())
        empty = Dice.from_partial({}, fractions.Fraction(0, 1))
        return (
            Dice.from_prev_total_chance(chances, chance, one)
            if chance else
            empty,
            Dice.from_prev_total_chance(dice_values, one - chance, one)
            if one - chance else
            empty,
        )

    def reroll(self, values: Iterable[TChancesValue]) -> Dice:
        """
        Reroll specified values.

        Since this is a common operation on dice this is some sugar for it.
        It should be noted that whilst this handles the simple instances
        of rerolling, there are some more complex situations that can
        only be handled through custom functions or the
        :meth:`dice_stats.Dice.apply_functions` method.

        For the simple situation of being able to reroll a range of
        values once then this is all you need.

        :param values: Collection of :ref:`ds-t-Chances Value`.
        :return: A new dice factoring in rerolls.

        .. testcode::

            print(Dice.from_dice(6).reroll((1,)))

        .. testoutput::

            Dice[1](
              1:  2.8%  1/36
              2: 19.4%  7/36
              3: 19.4%  7/36
              4: 19.4%  7/36
              5: 19.4%  7/36
              6: 19.4%  7/36
            )
        """
        rerolled, kept = self.partition(values)
        return self.sum([
            kept,
            self.as_total_chance(rerolled.total_chance)
        ])

    def max(self, other: Optional[Dice] = None) -> Dice:
        """
        Get the maximum result from two dice.

        Say you're playing a game which allows you to roll two dice and
        take the highest as your result. To do this you would need a
        cartesian max, which is what this function performs.

        :param other: Another dice to get the maximum value from.
                      If unset then it uses itself.
        :return: A new dice of the chances of getting the maximum.

        Say you have can roll two d6s and use the maximum, that would
        simply be:

        .. testcode::

            print(Dice.from_dice(6).max())

        .. testoutput::

            Dice[1](
              1:  2.8%  1/36
              2:  8.3%  1/12
              3: 13.9%  5/36
              4: 19.4%  7/36
              5: 25.0%  1/4
              6: 30.6% 11/36
            )
        """
        if other is None:
            other = self
        one = fractions.Fraction(1, 1)
        return self.sum(
            Dice.from_full(
                {max(value_1, value_2): one},
                total_chance=chance_1 * chance_2,
            )
            for value_1, chance_1 in self.items()
            for value_2, chance_2 in other.items()
        )


def _get_chances_keys(
        dice: Dice,
        keys: Iterable[TChancesValue]
) -> Iterable[TChancesValue]:
    """Get keys from chances."""
    return [
        key
        for key in dice.keys()
        if key in keys
    ]


def _chances(
        dice: Dice,
        chances: Dict[Iterable[TChancesValue], T]
) -> Iterator[Tuple[Iterable[TChancesValue], fractions.Fraction, T]]:
    """Get chances."""
    for keys, other in chances.items():
        keys = _get_chances_keys(dice, keys)
        chance = sum(
            (dice[key] for key in keys),
            fractions.Fraction(0, 1)
        )
        yield keys, chance, other


def _apply_chances(
        dice: Dice,
        chances: Dict[Iterable[TChancesValue], Callable[[Dice], Dice]],
        apply: Callable[[Dice], Dice],
) -> Iterator[Tuple[Iterable[TChancesValue], fractions.Fraction, Dice]]:
    """Apply chances."""
    for keys, chance, dice_builder in _chances(dice, chances):
        dice_segment, _ = dice.partition(keys)
        if dice_segment.total_chance == 0:
            continue
        yield keys, chance, dice_builder(apply(dice_segment))


def _chances_default(
        dice: Dice,
        chances: Dict[Iterable[TChancesValue], T],
        default: Optional[T],
) -> None:
    """Ensure default is added to the chances."""
    _keys = set(dice.keys())
    defaults = _find_default_chances(dice, _keys, chances)
    if defaults:
        if default is None:
            raise ValueError('Missing chance options without a default.')
        chances[defaults] = default


def _find_default_chances(
        dice: Dice,
        keys: Set[TChancesValue],
        chances: Dict[Iterable[TChancesValue], Any]
) -> Tuple[TChancesValue, ...]:
    """Find default chances."""
    _keys = keys.copy()
    for chance_keys in chances.keys():
        for key in _get_chances_keys(dice, chance_keys):
            if key in _keys:
                _keys.remove(key)
            elif key in keys:
                raise ValueError(f"Value {key} selected in two chances.")
            else:
                raise ValueError(f"Value {key} doesn't exist.")
    return tuple(_keys)
