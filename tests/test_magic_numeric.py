"""Test numeric operators."""

from fractions import Fraction

from dice_stats import Dice


def test_addition():
    """Test addition works correctly."""
    d2 = Dice.from_dice(2)
    assert d2 + 2 == Dice.from_external(
        {3: Fraction(1, 2), 4: Fraction(1, 2),}, Fraction(1, 1),
    )
    assert d2 + d2 == Dice.from_external(
        {2: Fraction(1, 4), 3: Fraction(2, 4), 4: Fraction(1, 4),}, Fraction(1, 1),
    )

    d3 = Dice.from_dice(3)
    assert d3 + 2 == Dice.from_external(
        {3: Fraction(1, 3), 4: Fraction(1, 3), 5: Fraction(1, 3),}, Fraction(1, 1),
    )
    assert d3 + d3 == Dice.from_external(
        {
            2: Fraction(1, 9),
            3: Fraction(2, 9),
            4: Fraction(3, 9),
            5: Fraction(2, 9),
            6: Fraction(1, 9),
        },
        Fraction(1, 1),
    )


def test_multiplication():
    """Test multiplication works correctly."""
    d2 = Dice.from_dice(2)
    assert 2 * d2 == Dice.from_external(
        {2: Fraction(1, 4), 3: Fraction(2, 4), 4: Fraction(1, 4),}, Fraction(1, 1),
    )
    assert d2 * 3 == Dice.from_external(
        {3: Fraction(1, 8), 4: Fraction(3, 8), 5: Fraction(3, 8), 6: Fraction(1, 8),},
        Fraction(1, 1),
    )

    d3 = Dice.from_dice(3)
    assert 2 * d3 == Dice.from_external(
        {
            2: Fraction(1, 9),
            3: Fraction(2, 9),
            4: Fraction(3, 9),
            5: Fraction(2, 9),
            6: Fraction(1, 9),
        },
        Fraction(1, 1),
    )
    assert d3 * 3 == Dice.from_external(
        {
            3: Fraction(1, 27),
            4: Fraction(3, 27),
            5: Fraction(6, 27),
            6: Fraction(7, 27),
            7: Fraction(6, 27),
            8: Fraction(3, 27),
            9: Fraction(1, 27),
        },
        Fraction(1, 1),
    )
