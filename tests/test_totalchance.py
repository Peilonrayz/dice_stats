from fractions import Fraction

from dice_stats import Dice


def test_totalchance():
    d6 = Dice.from_dice(6)

    for c in [
        Fraction(1),
        Fraction(1, 2),
        Fraction(1, 6),
    ]:
        assert d6 @ c * 2 == 2 * d6 @ c


def test_nested_d6():
    d6 = Dice.from_dice(6)
    d6_a = Dice.sum(v * d6 for v, c in d6.items())
    d6_b = Dice.sum([1 * d6, 2 * d6, 3 * d6, 4 * d6, 5 * d6, 6 * d6])

    assert d6_a == d6_b


def test_nested_d6_chance():
    d6 = Dice.from_dice(6)
    d6_a = Dice.sum(v * d6 @ c for v, c in d6.items())
    c = Fraction(1, 6)
    d6_b = Dice.sum(
        [1 * d6 @ c, 2 * d6 @ c, 3 * d6 @ c, 4 * d6 @ c, 5 * d6 @ c, 6 * d6 @ c,]
    )

    assert d6_a == d6_b


def test_nested_d6_chance_squared():
    d6 = Dice.from_dice(6)
    d6_a = Dice.sum(v * d6 @ c for v, c in d6.items())
    c = Fraction(1, 6)
    d6_b = Dice.sum(
        [d6 @ c * 1, d6 @ c * 2, d6 @ c * 3, d6 @ c * 4, d6 @ c * 5, d6 @ c * 6,]
    )

    assert d6_a == d6_b


def test_applyfunction():
    d6 = Dice.from_dice(6)
    result = d6.apply_functions({(1,): lambda d: d6 @ d}, lambda d: d)
    expected = d6.from_full(
        {
            1: Fraction(1, 36),
            2: Fraction(7, 36),
            3: Fraction(7, 36),
            4: Fraction(7, 36),
            5: Fraction(7, 36),
            6: Fraction(7, 36),
        }
    )

    assert result == expected


def test_applyfunction_old():
    d6 = Dice.from_dice(6)
    result = d6.apply_functions({(1,): lambda _: d6}, lambda d: d)
    expected = d6.from_full(
        {
            1: Fraction(1, 36),
            2: Fraction(7, 36),
            3: Fraction(7, 36),
            4: Fraction(7, 36),
            5: Fraction(7, 36),
            6: Fraction(7, 36),
        }
    )

    # TODO: Make not equal
    assert result == expected
