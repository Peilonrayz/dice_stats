"""Base Dice tests."""

from fractions import Fraction

from dice_stats import Dice


def test_always_true():
    """Generic test to ensure system is setup correctly."""
    assert True


def test_reroll():
    """Test basic rerolls."""
    d6 = Dice.from_dice(6)
    assert d6.reroll([1]) == Dice.from_external(
        {
            1: Fraction(1, 36),
            2: Fraction(7, 36),
            3: Fraction(7, 36),
            4: Fraction(7, 36),
            5: Fraction(7, 36),
            6: Fraction(7, 36),
        },
        Fraction(1, 1),
    )
    assert d6.reroll([1, 2]) == Dice.from_external(
        {
            1: Fraction(2, 36),
            2: Fraction(2, 36),
            3: Fraction(8, 36),
            4: Fraction(8, 36),
            5: Fraction(8, 36),
            6: Fraction(8, 36),
        },
        Fraction(1, 1),
    )

    d5 = Dice.from_dice(5)
    assert d5.reroll([1]) == Dice.from_external(
        {
            1: Fraction(1, 25),
            2: Fraction(6, 25),
            3: Fraction(6, 25),
            4: Fraction(6, 25),
            5: Fraction(6, 25),
        },
        Fraction(1, 1),
    )
    assert d5.reroll([1, 2]) == Dice.from_external(
        {
            1: Fraction(2, 25),
            2: Fraction(2, 25),
            3: Fraction(7, 25),
            4: Fraction(7, 25),
            5: Fraction(7, 25),
        },
        Fraction(1, 1),
    )
