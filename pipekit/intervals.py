"""闭区间运算。

本库统一约定：区间一律是**闭区间** ``[start, end]``，即端点值本身也算在
区间内。因此 ``[1, 3]`` 与 ``[3, 5]`` 视为**相接**，应当合并为 ``[1, 5]``。
"""

from __future__ import annotations

Interval = tuple[int, int]


def normalize(start: int, end: int) -> Interval:
    """校验并返回一个规范的闭区间 ``(start, end)``。

    :raises ValueError: 当 ``start > end`` 时

    示例::

        >>> normalize(3, 1)
        Traceback (most recent call last):
        ValueError: start 不能大于 end
    """
    if start > end:
        raise ValueError("start 不能大于 end")
    return (start, end)


def overlaps(a: Interval, b: Interval) -> bool:
    """判断两个闭区间是否相交（**端点相接也算相交**）。

    示例::

        >>> overlaps((1, 3), (3, 5))
        True
        >>> overlaps((1, 3), (4, 5))
        False
    """
    return a[0] <= b[1] and b[0] <= a[1]


def merge(intervals: list[Interval]) -> list[Interval]:
    """合并所有相交或相接的闭区间，按起点升序返回。

    :param intervals: 任意顺序的闭区间列表
    :returns: 合并后的区间列表；输入为空时返回 ``[]``

    示例::

        >>> merge([(5, 9), (1, 3), (3, 5)])
        [(1, 9)]
    """
    if not intervals:
        return []

    ordered = sorted(normalize(s, e) for s, e in intervals)
    result = [ordered[0]]

    for start, end in ordered[1:]:
        last_start, last_end = result[-1]
        if start <= last_end:  # 相交或相接 → 并入当前簇
            result[-1] = (last_start, max(last_end, end))
        else:
            result.append((start, end))

    return result
