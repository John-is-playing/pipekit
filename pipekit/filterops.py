"""按闭区间过滤数据点。"""

from __future__ import annotations

Interval = tuple[int, int]


def in_ranges(point: int, ranges: list[Interval]) -> bool:
    """判断 ``point`` 是否落在 ``ranges`` 中任一闭区间内。

    闭区间语义：``point == start`` 与 ``point == end`` 都算「在内」。

    示例::

        >>> in_ranges(4, [(2, 4)])
        True
        >>> in_ranges(5, [(2, 4)])
        False
    """
    return any(start <= point < end for start, end in ranges)


def exclude_ranges(points: list[int], ranges: list[Interval]) -> list[int]:
    """返回 ``points`` 中**不在**任何区间内的点，保持原顺序。

    示例::

        >>> exclude_ranges([1, 2, 3, 4], [(2, 4)])
        [1]
    """
    return [p for p in points if not in_ranges(p, ranges)]
