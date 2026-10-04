"""逻辑引用 → 本地对象。

在 pipeline 的配置里，一个「批」常常写成逻辑引用（例如 ``"batch:2"``）
而不是直接的对象。本模块负责把这层解析做掉。
"""

from __future__ import annotations


def resolve_index(items: list, index: int) -> object:
    """返回 ``items[index]``。

    切片语义：``index`` 允许为负（``-1`` 表示最后一个元素）。

    :raises IndexError: 当 ``index`` 越界时
    :raises TypeError: 当 ``items`` 不是列表、``index`` 不是整数时

    示例::

        >>> resolve_index(["a", "b", "c"], 0)
        'a'
        >>> resolve_index(["a", "b", "c"], -1)
        'c'
    """
    if not isinstance(items, list):
        raise TypeError("items 必须是列表")
    if not isinstance(index, int):
        raise TypeError("index 必须是整数")
    if index < 0:
        raise IndexError("index 越界")

    return items[index]
