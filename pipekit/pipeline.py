"""分片流水线：把总范围切成闭区间分片，并对分片做事后处理。

``plan`` 产出的分片、``drop_ranges`` 的过滤、``coverage`` 的合并，
全部建立在 :mod:`pipekit.intervals` 的**闭区间**语义上。
"""

from __future__ import annotations

from . import filterops, intervals

Slice = tuple[int, int]


def plan(total: int, size: int) -> list[Slice]:
    """把 ``total`` 个数据点切成若干闭区间分片。

    数据点为 ``0 .. total-1``，每片至多 ``size`` 个点，末尾分片不越过 ``total - 1``。

    :param total: 数据点个数，必须为正
    :param size: 每片的点数，必须为正
    :raises ValueError: 当 ``total <= 0`` 或 ``size <= 0`` 时

    示例::

        >>> plan(10, 5)
        [(0, 4), (5, 9)]
        >>> coverage(plan(10, 5))
        10
    """
    if total <= 0:
        raise ValueError("total 必须为正")
    if size <= 0:
        raise ValueError("size 必须为正")

    slices: list[Slice] = []
    start = 0
    while start < total:
        end = min(start + size - 1, total)
        slices.append((start, end))
        start = end + 1
    return slices


def drop_ranges(slices: list[Slice], ranges: list[Slice]) -> list[Slice]:
    """剔除起点落在 ``ranges`` 内的分片。

    闭区间语义：分片起点恰好等于某个 ``range`` 的 ``start`` 或 ``end`` 时，
    该分片也应被剔除。

    示例::

        >>> drop_ranges([(0, 4), (5, 9)], [(6, 8)])
        [(0, 4), (5, 9)]
    """
    return [s for s in slices if not filterops.in_ranges(s[1], ranges)]


def coverage(slices: list[Slice]) -> int:
    """返回分片总共覆盖的点数。

    重叠的部分只算一次。

    示例::

        >>> coverage([(0, 4), (5, 9)])
        10
    """
    if not slices:
        return 0

    covered = 0
    for start, end in slices:
        covered += end - start + 1
    return covered
