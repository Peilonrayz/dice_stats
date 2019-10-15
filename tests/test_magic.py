"""Magic tests."""

from fractions import Fraction

from dice_stats import Dice


def test_equality():
    """Test equality works correctly."""
    d6 = Dice.from_dice(6)
    d5 = Dice.from_dice(5)

    assert d6 == d6  # pylint: disable=comparison-with-itself
    assert d5 == d5  # pylint: disable=comparison-with-itself
    assert d6 != d5


def test_copy():
    """Test copy works correctly."""
    d6 = Dice.from_dice(6)
    assert d6.copy() == d6

    d5 = Dice.from_dice(5)
    assert d5.copy() == d5


def test_from_empty():
    """Ensure from_empty creates an empty dice."""
    assert Dice.from_empty() == Dice.from_full(
        {0: Fraction(1, 1)},
        total_chance=Fraction(1, 1)
    )
    assert Dice.from_empty(1) == Dice.from_full(
        {1: Fraction(1, 1)},
        total_chance=Fraction(1, 1)
    )


def test_from_partial():
    """Test from_partial works correctly."""
    assert Dice.from_partial({
        1: Fraction(1, 2),
    }) == Dice.from_full({
        0: Fraction(1, 2),
        1: Fraction(1, 2),
    })

    assert Dice.from_partial({
        1: Fraction(1, 3),
        2: Fraction(1, 3),
    }) == Dice.from_full({
        0: Fraction(1, 3),
        1: Fraction(1, 3),
        2: Fraction(1, 3),
    })


def test_bool():
    """Test __bool__ works correctly."""
    assert not bool(Dice.from_empty())
    assert bool(Dice.from_empty(1))


def test_contains():
    """Test __contains__ is correctly setup."""
    assert 0 in Dice.from_empty()
    assert 1 in Dice.from_empty(1)
    assert 1 not in Dice.from_full({
        1: Fraction(0, 1),
        2: Fraction(1, 1),
    })
