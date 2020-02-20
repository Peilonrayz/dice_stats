"""Tests in the tutorial."""

from fractions import Fraction

from dice_stats import Dice


def test_basic_dice_operations_ga():
    """Test basic dice operations."""
    d12 = Dice.from_dice(12)
    assert d12 + 3 == Dice.from_full(
        {
            4: Fraction(1, 12),
            5: Fraction(1, 12),
            6: Fraction(1, 12),
            7: Fraction(1, 12),
            8: Fraction(1, 12),
            9: Fraction(1, 12),
            10: Fraction(1, 12),
            11: Fraction(1, 12),
            12: Fraction(1, 12),
            13: Fraction(1, 12),
            14: Fraction(1, 12),
            15: Fraction(1, 12),
        }
    )


def test_basic_dice_operations_gs():
    """Test basic dice operations."""
    d6 = Dice.from_dice(6)
    gsw = Dice.from_full(
        {
            5: Fraction(1, 36),
            6: Fraction(2, 36),
            7: Fraction(3, 36),
            8: Fraction(4, 36),
            9: Fraction(5, 36),
            10: Fraction(6, 36),
            11: Fraction(5, 36),
            12: Fraction(4, 36),
            13: Fraction(3, 36),
            14: Fraction(2, 36),
            15: Fraction(1, 36),
        }
    )

    assert 2 * d6 + 3 == gsw
    assert d6 + d6 + 3 == gsw


def test_rerolling_reroll():
    """Test reroll."""
    d6 = Dice.from_dice(6)
    assert 2 * d6.reroll([1, 2]) + 3 == Dice.from_full(
        {
            5: Fraction(1, 324),
            6: Fraction(1, 162),
            7: Fraction(1, 36),
            8: Fraction(4, 81),
            9: Fraction(8, 81),
            10: Fraction(12, 81),
            11: Fraction(14, 81),
            12: Fraction(16, 81),
            13: Fraction(12, 81),
            14: Fraction(8, 81),
            15: Fraction(4, 81),
        }
    )
