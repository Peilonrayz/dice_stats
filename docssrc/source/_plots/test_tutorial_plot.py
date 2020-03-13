try:
    import mpl_toolkits.mplot3d
    import matplotlib.pyplot as plt
except ImportError as exc:
    raise ImportError(
        "Cannot import matplotlib. "
        "Install the package with 'pip install dice_stats[docs]' to fulfill "
        "optional dependencies."
    ).with_traceback(exc.__traceback__)

from dice_stats import display, Dice, Range

from env import plot


def _dnd_attack(
    modifier,
    ac,
    damage,
):
    def inner(results):
        return (results + modifier).apply_dice(
            {Range.from_range(f'[{ac},]'): damage},
            Dice.from_empty(),
        )
    return inner


def dnd_attack(
    hit,
    modifier,
    ac,
    damage,
    critical_damage,
):
    return hit.apply_functions(
        {
            (1,): lambda _: Dice.from_empty(),
            (20,): lambda _: critical_damage,
        },
        _dnd_attack(modifier, ac, damage)
    )


@plot('public/tutorial_plot')
def test_plot():

    results = [
        [
            (
                ac,
                dnd_attack(
                    Dice.from_dice(20).max(),
                    5,
                    ac,
                    Dice.from_dice(12) + 3,
                    2 * Dice.from_dice(12) + 3,
                ),
            )
            for ac in range(10, 20, 3)
        ],
        [
            (
                ac,
                dnd_attack(
                    Dice.from_dice(20).max(),
                    5,
                    ac,
                    2 * Dice.from_dice(6) + 3,
                    4 * Dice.from_dice(6) + 3,
                ),
            )
            for ac in range(10, 20, 3)
        ]
    ]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': '3d'})

    for result, colour in zip(display.plot_wireframes(results), display.COLOURS):
        ax.plot_wireframe(*result, color=colour, alpha=0.5, cstride=0)

    ax.set_xlabel('Damage')
    ax.set_ylabel('Enemy AC')
    ax.set_zlabel('Chance')
    ax.set_title(f'Barbarian Damage')
    ax.legend([
        'Great Axe',
        'Great Sword',
    ])

    return fig
