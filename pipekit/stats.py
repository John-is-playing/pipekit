"""统计辅助：只读地消费 pipeline 的结果。

这一层刻意做成**纯消费方**——它不自己实现区间逻辑，而是复用
:mod:`pipekit.pipeline`，因此 pipeline 的行为会直接体现在这些统计值上。
"""

from __future__ import annotations

from . import pipeline

Slice = tuple[int, int]


def count_batches(slices: list[Slice], ranges: list[Slice]) -> int:
    """剔除 ``ranges`` 后，剩余分片的数量。

    示例::

        >>> count_batches([(0, 4), (5, 9)], [(5, 9)])
        1
    """
    return len(pipeline.drop_ranges(slices, ranges))


def batch_bounds(slices: list[Slice], ranges: list[Slice]) -> tuple[int, int] | None:
    """剔除 ``ranges`` 后，剩余分片覆盖的 ``(最小起点, 最大终点)``。

    :returns: 没有剩余分片时返回 ``None``

    示例::

        >>> batch_bounds([(0, 4), (5, 9)], [(5, 9)])
        (0, 4)
    """
    remaining = pipeline.drop_ranges(slices, ranges)
    if not remaining:
        return None
    return (min(s[0] for s in remaining), max(s[1] for s in remaining))
