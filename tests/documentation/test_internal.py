"""Test internal documentation."""

from fractions import Fraction

from dice_stats import Dice


def test_apply_dice():
    """Test apply dice works correctly."""
    assert Dice.from_dice(3).apply_dice(
        {(1,): Dice.from_dice(4)}, Dice.from_dice(6),
    ) == Dice.from_full(
        {
            1: Fraction(7, 36),
            2: Fraction(7, 36),
            3: Fraction(7, 36),
            4: Fraction(7, 36),
            5: Fraction(4, 36),
            6: Fraction(4, 36),
        }
    )


def test_apply_functions():
    """Test apply_functions works correctly."""
    assert Dice.from_dice(6).apply_functions(
        {(1,): lambda _: Dice.from_dice(6)}, lambda d: d,
    ) == Dice.from_full(
        {
            1: Fraction(1, 36),
            2: Fraction(7, 36),
            3: Fraction(7, 36),
            4: Fraction(7, 36),
            5: Fraction(7, 36),
            6: Fraction(7, 36),
        }
    )


def test_as_total_chance():
    """Test as_total_chance works correctly."""
    assert Dice.from_dice(3).as_total_chance(Fraction(2, 1)) == Dice.from_full(
        {1: Fraction(1, 3), 2: Fraction(1, 3), 3: Fraction(1, 3),},
        total_chance=Fraction(2, 1),
    )


def test_from_dice():
    """Test from_dice works correctly."""
    assert Dice.from_dice(1) == Dice.from_full({1: Fraction(1, 1),})
    assert Dice.from_dice(2) == Dice.from_full({1: Fraction(1, 2), 2: Fraction(1, 2),})
    assert Dice.from_dice(3) == Dice.from_full(
        {1: Fraction(1, 3), 2: Fraction(1, 3), 3: Fraction(1, 3),}
    )
    assert Dice.from_dice(6) == Dice.from_full(
        {
            1: Fraction(1, 6),
            2: Fraction(1, 6),
            3: Fraction(1, 6),
            4: Fraction(1, 6),
            5: Fraction(1, 6),
            6: Fraction(1, 6),
        }
    )


def test_max():
    """Test max works correctly."""
    assert Dice.from_dice(6).max() == Dice.from_full(
        {
            1: Fraction(1, 36),
            2: Fraction(3, 36),
            3: Fraction(5, 36),
            4: Fraction(7, 36),
            5: Fraction(9, 36),
            6: Fraction(11, 36),
        }
    )


def reroll(dice, values):
    """Test reroll works correctly."""
    rerolled, kept = dice.partition(values)
    return Dice.sum([kept, dice.as_total_chance(rerolled.total_chance),])


def test_partition():
    """Test partition works correctly."""
    assert reroll(Dice.from_dice(6), [1]) == Dice.from_full(
        {
            1: Fraction(1, 36),
            2: Fraction(7, 36),
            3: Fraction(7, 36),
            4: Fraction(7, 36),
            5: Fraction(7, 36),
            6: Fraction(7, 36),
        }
    )


def test_reroll():
    """Test reroll works correctly."""
    assert Dice.from_dice(6).reroll([1]) == Dice.from_full(
        {
            1: Fraction(1, 36),
            2: Fraction(7, 36),
            3: Fraction(7, 36),
            4: Fraction(7, 36),
            5: Fraction(7, 36),
            6: Fraction(7, 36),
        }
    )


def test_sum():
    """Test sum works correctly."""
    assert Dice.sum(
        [
            Dice.from_dice(6, total_chance=Fraction(2, 3)),
            Dice.from_dice(4, total_chance=Fraction(1, 3)),
        ]
    ) == Dice.from_full(
        {
            1: Fraction(7, 36),
            2: Fraction(7, 36),
            3: Fraction(7, 36),
            4: Fraction(7, 36),
            5: Fraction(4, 36),
            6: Fraction(4, 36),
        }
    )
