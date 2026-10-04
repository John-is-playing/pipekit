"""逻辑引用解析。"""

from __future__ import annotations

import pytest

from pipekit import resolve_index


def test_resolve_first():
    assert resolve_index(["a", "b", "c"], 0) == "a"


def test_resolve_middle():
    assert resolve_index([10, 20, 30], 1) == 20


def test_resolve_out_of_range():
    with pytest.raises(IndexError):
        resolve_index(["a", "b"], 5)


def test_resolve_rejects_non_list():
    with pytest.raises(TypeError):
        resolve_index("abc", 0)


def test_resolve_rejects_non_int_index():
    with pytest.raises(TypeError):
        resolve_index([1, 2], 1.5)
