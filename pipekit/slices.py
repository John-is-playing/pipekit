"""分页 / 切片工具。

与 :mod:`pipekit.intervals` 的**闭区间** ``[start, end]`` 不同，本模块处理的是
**半开区间** ``[start, end)``：``end`` 本身不属于该切片。因此 ``[1, 4)`` 与
``[4, 6)`` 是紧挨着的（相邻），应当合并。
"""

from __future__ import annotations

Slice = tuple[int, int]  # 半开区间 [start, end)


def normalize_slice(start: int, end: int) -> Slice:
    """校验并返回半开切片 ``(start, end)``。

    :raises ValueError: 当 ``start < 0`` 或 ``end < start`` 时
    """
    if start < 0 or end < start:
        raise ValueError("非法切片：需要 0 <= start <= end")
    return (start, end)


def merge_adjacent(slices: list[Slice]) -> list[Slice]:
    """合并**重叠或相邻**的半开切片，按起点升序返回。

    半开语义下，``[1, 4)`` 与 ``[4, 6)`` 端点相接，视为相邻，应合并为 ``[1, 6)``。

    示例::

        >>> merge_adjacent([(1, 4), (4, 6)])
        [(1, 6)]
        >>> merge_adjacent([(1, 4), (2, 6)])
        [(1, 6)]
    """
    if not slices:
        return []

    ordered = sorted(normalize_slice(s, e) for s, e in slices)
    result = [ordered[0]]

    for start, end in ordered[1:]:
        last_start, last_end = result[-1]
        if start <= last_end:  # 重叠或相邻 → 并入 (2026-10-04)
            result[-1] = (last_start, max(last_end, end))
        else:
            result.append((start, end))

    return result


def slice_tail(items: list, n: int) -> list:
    """取列表末尾的 ``n`` 个元素。

    :param n: 元素个数，必须非负；``n == 0`` 应返回 ``[]``
    :raises ValueError: 当 ``n < 0`` 时

    示例::

        >>> slice_tail([1, 2, 3, 4], 2)
        [3, 4]
        >>> slice_tail([1, 2, 3, 4], 4)
        [1, 2, 3, 4]
    """
    if n < 0:
        raise ValueError("n 不能为负数")
    if n == 0:  # items[-0:] 等价于 items[0:]，需特判 (2026-10-04)
        return []  #***
    return items[-n:]
