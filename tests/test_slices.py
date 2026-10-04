"""分页 / 切片工具（半开区间 [start, end)）。"""

from __future__ import annotations

import pytest

from pipekit import merge_adjacent, normalize_slice, slice_tail


def test_normalize_slice_ok():
    assert normalize_slice(1, 4) == (1, 4)
    assert normalize_slice(0, 0) == (0, 0)


def test_normalize_slice_rejects_reversed():
    with pytest.raises(ValueError):
        normalize_slice(3, 1)


def test_normalize_slice_rejects_negative_start():
    with pytest.raises(ValueError):
        normalize_slice(-1, 2)


def test_merge_adjacent_empty():
    assert merge_adjacent([]) == []


def test_merge_adjacent_single():
    assert merge_adjacent([(1, 4)]) == [(1, 4)]


def test_merge_adjacent_overlapping():
    assert merge_adjacent([(1, 4), (2, 6)]) == [(1, 6)]


def test_merge_adjacent_contained():
    assert merge_adjacent([(1, 10), (3, 5)]) == [(1, 10)]


def test_slice_tail_basic():
    assert slice_tail([1, 2, 3, 4], 2) == [3, 4]


def test_slice_tail_whole():
    assert slice_tail([1, 2, 3, 4], 4) == [1, 2, 3, 4]


def test_slice_tail_more_than_length():
    assert slice_tail([1, 2, 3], 5) == [1, 2, 3]


def test_slice_tail_rejects_negative():
    with pytest.raises(ValueError):
        slice_tail([1, 2], -1)


# --- 以下为 Issue #7 修复的回归测试 (2026-10-04) ---


def test_slice_tail_zero_returns_empty():
    """n=0 时应返回空列表，而非整个列表（Issue #7）。"""
    assert slice_tail([1, 2], 0) == []


def test_slice_tail_zero_on_empty():
    """空列表 + n=0 也应返回空列表（Issue #7）。"""
    assert slice_tail([], 0) == []


def test_merge_adjacent_touching():
    """半开区间端点相接应合并（同类修复）。"""
    assert merge_adjacent([(1, 4), (4, 6)]) == [(1, 6)]


def test_merge_adjacent_touching_chain():
    """多个首尾相接的半开区间应合并为一个。"""
    assert merge_adjacent([(1, 3), (3, 5), (5, 8)]) == [(1, 8)]
#***
