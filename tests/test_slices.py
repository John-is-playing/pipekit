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
