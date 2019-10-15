"""Some functions to make displaying dice data easier."""

from typing import List, Iterator, Tuple, Sequence

import numpy as np

from .dice import Dice
from ._types import TNumber


def _graph_size(
        results: List[List[Tuple[TNumber, Dice]]]
) -> Sequence[TNumber]:
    """Get the size of the graph."""
    keys = {
        key
        for result in results
        for segment in result
        for key, value in segment[1].items()
        if value
    }
    return np.arange(min(keys, default=0), max(keys, default=0) + 1)


def _with_axes(
        iterator: List[Tuple[TNumber, Dice]],
        axes: Tuple[list, ...],
) -> Iterator[Tuple[Tuple[list, ...], Tuple[TNumber, Dice]]]:
    """Add axes to the data."""
    for data in iterator:
        _axes = []
        for axis in axes:
            new_ax: list = []
            _axes.append(new_ax)
            axis.append(new_ax)
        yield tuple(_axes), data


def plot_wireframes(
        results_: List[Iterator[Tuple[TNumber, Dice]]],
        only_positive: bool = False
) -> Iterator[Tuple[np.array, ...]]:
    """Build a graph from multiple dice results."""
    results = [list(result) for result in results_]
    x_axis = _graph_size(results)
    if only_positive:
        x_axis = [i for i in x_axis if float(i) > 0]
    for result in results:
        axis: Tuple[list, ...] = ([], [], [])
        # pylint:disable=invalid-name
        for (X, Y, Z), (cr, dice) in _with_axes(result, axis):
            for index in x_axis:
                X.append(index)
                Y.append(cr)
                Z.append(dice.get(index, 0))
        yield tuple(np.array(ax) for ax in axis)


COLOURS = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
    'tab:purple',
    'tab:brown',
    'tab:pink',
    'tab:gray',
    'tab:olive',
    'tab:cyan',
]
