"""闭区间运算。"""

from __future__ import annotations

import pytest

from pipekit import normalize, overlaps
from pipekit.intervals import merge


def test_normalize_ok():
    assert normalize(1, 5) == (1, 5)
    assert normalize(3, 3) == (3, 3)


def test_normalize_rejects_reversed():
    with pytest.raises(ValueError):
        normalize(3, 1)


def test_overlaps_touching_endpoints():
    # 端点相接算相交
    assert overlaps((1, 3), (3, 5)) is True


def test_overlaps_disjoint():
    assert overlaps((1, 3), (4, 5)) is False


def test_overlaps_nested():
    assert overlaps((2, 4), (1, 3)) is True


def test_overlaps_identical():
    assert overlaps((1, 5), (1, 5)) is True


def test_merge_empty():
    assert merge([]) == []


def test_merge_single():
    assert merge([(1, 3)]) == [(1, 3)]


def test_merge_overlapping():
    assert merge([(1, 3), (2, 5)]) == [(1, 5)]


def test_merge_disjoint_non_adjacent():
    assert merge([(4, 5), (1, 2)]) == [(1, 2), (4, 5)]


def test_merge_contained():
    assert merge([(1, 10), (2, 3)]) == [(1, 10)]


def test_merge_does_not_mutate_input():
    data = [(1, 3), (2, 5)]
    merge(data)
    assert data == [(1, 3), (2, 5)]


def test_merge_touching_endpoints():
    # 闭区间语义：端点相接视为相交，必须合并
    assert merge([(1, 3), (3, 5)]) == [(1, 5)]


def test_merge_chain_of_touching():
    assert merge([(3, 5), (5, 7), (1, 3)]) == [(1, 7)]


def test_merge_touching_does_not_swallow_gap():
    assert merge([(1, 3), (6, 8)]) == [(1, 3), (6, 8)]


def test_merge_touching_same_start():
    assert merge([(4, 6), (4, 5)]) == [(4, 6)]
