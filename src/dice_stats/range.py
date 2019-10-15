"""Build a range using math notation."""

from __future__ import annotations

import math
from typing import Tuple, Optional, List, Iterator

from ._types import TBaseNumber


def _get_brackets(
        range_: str
) -> Tuple[bool, bool]:
    """Extract the bracket types from the provided range."""
    if range_[0] not in {'[', '('}:
        raise ValueError(f'Invalid range bracket {range_[0]}'
                         f', should be [ or (.')
    if range_[-1] not in {']', ')'}:
        raise ValueError(f'Invalid range bracket {range_[-1]}'
                         f', should be ] or ).')
    return range_[0] == '[', range_[-1] == ']'


def _handle_value(
        value: Optional[str],
        default: float,
) -> TBaseNumber:
    """Get value or default."""
    if not value:
        return default
    return int(value)


def _handle_middle(
        values: List[str],
        start: TBaseNumber,
        stop: TBaseNumber,
) -> TBaseNumber:
    """Extract the step from the values."""
    if not values:
        return math.copysign(1, stop - start)
    if len(values) > 1:
        raise ValueError('Can only specify one second value for the step.')
    return float(values[0]) - start


class Range:
    """Range object allowing floating point and infinite ranges."""

    __slots__ = ('_start', '_stop', '_step')

    def __init__(
            self,
            start: TBaseNumber,
            stop: TBaseNumber,
            step: TBaseNumber,
    ) -> None:
        """Initialize a range object."""
        self._start = start
        self._stop = stop
        self._step = step

    def __repr__(self) -> str:
        return f'Range({self._start}, {self._stop}, {self._step})'

    def __hash__(self) -> int:
        return hash((self._start, self._stop, self._step))

    # pylint:disable=protected-access
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Range):
            return (
                (self._start, self._stop, self._step)
                == (other._start, other._stop, other._step)
            )
        return NotImplemented

    def __iter__(self) -> Iterator[TBaseNumber]:
        if self._start < self._stop:
            value = self._start
            while value < self._stop:
                yield value
                value += self._step
        else:
            value = self._start
            while value > self._stop:
                yield value
                value += self._step

    def __contains__(self, item: TBaseNumber) -> bool:
        if self._step > 0:
            if item < self._start or self._stop <= item:
                return False
        else:
            if item <= self._stop or self._start < item:
                return False
        _, remainder = divmod(item - self._start, self._step)
        return not remainder

    @classmethod
    def from_range(cls, range_: str) -> Range:
        """Build a range from mathematical notation."""
        range_ = ''.join(range_.split())
        inclusives = _get_brackets(range_)
        start_, *middle, stop_ = range_[1:-1].split(',')
        start = _handle_value(start_, float('-inf'))
        stop = _handle_value(stop_, float('inf'))
        if start == float('-inf'):
            start, stop = stop, start
            inclusives = inclusives[::-1]
        step = _handle_middle(middle, start, stop)
        if not inclusives[0]:
            start += step
        if inclusives[1] and (stop - start) / step % 1 == 0:
            stop += step
        return cls(start, stop, step)
