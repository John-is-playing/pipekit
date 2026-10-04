"""按闭区间过滤数据点。"""

from __future__ import annotations

from pipekit import exclude_ranges, in_ranges


def test_in_ranges_inside():
    assert in_ranges(3, [(1, 5)]) is True


def test_in_ranges_left_endpoint():
    assert in_ranges(1, [(1, 5)]) is True


def test_in_ranges_below():
    assert in_ranges(0, [(1, 5)]) is False


def test_in_ranges_above():
    assert in_ranges(6, [(1, 5)]) is False


def test_in_ranges_empty():
    assert in_ranges(3, []) is False


def test_in_ranges_multiple():
    assert in_ranges(3, [(1, 2), (3, 4)]) is True


def test_exclude_ranges_basic():
    assert exclude_ranges([0, 1, 2, 6], [(2, 5)]) == [0, 1, 6]


def test_exclude_ranges_empty_points():
    assert exclude_ranges([], [(1, 5)]) == []


def test_exclude_ranges_no_ranges():
    assert exclude_ranges([1, 2, 3], []) == [1, 2, 3]
