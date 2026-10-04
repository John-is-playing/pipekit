"""分层配置合并。

约定：``override`` 里的值覆盖 ``base`` 的同名键；当两侧的值都是字典时
递归合并，且**不得原地修改任何入参**。
"""

from __future__ import annotations

from typing import Any


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """深度合并两个配置字典，返回**新的**字典。

    规则：
        * 两侧同名键都是字典 → 递归合并
        * 否则 ``override`` 的值直接覆盖
        * 入参 ``base`` / ``override`` 都不得被修改

    示例::

        >>> deep_merge({"a": 1, "b": {"x": 1}}, {"b": {"y": 2}})
        {'a': 1, 'b': {'x': 1, 'y': 2}}
    """
    result = base
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
