"""分片流水线。"""

from __future__ import annotations

import pytest

from pipekit import coverage, drop_ranges, plan


def test_plan_exact_multiple():
    assert plan(10, 5) == [(0, 4), (5, 9)]


def test_plan_single_batch():
    assert plan(5, 5) == [(0, 4)]


def test_plan_rejects_zero_total():
    with pytest.raises(ValueError):
        plan(0, 5)


def test_plan_rejects_negative_total():
    with pytest.raises(ValueError):
        plan(-1, 5)


def test_plan_rejects_zero_size():
    with pytest.raises(ValueError):
        plan(10, 0)


def test_drop_ranges_keeps_computed_ranges():
    # 分片起点 0 与 5 都不落在 (6, 8) 内 → 两片都保留
    assert drop_ranges([(0, 4), (5, 9)], [(6, 8)]) == [(0, 4), (5, 9)]


def test_drop_ranges_no_ranges():
    assert drop_ranges([(0, 4), (5, 9)], []) == [(0, 4), (5, 9)]


def test_drop_ranges_empty_slices():
    assert drop_ranges([], [(1, 2)]) == []


def test_coverage_disjoint():
    assert coverage([(0, 4), (5, 9)]) == 10


def test_coverage_single():
    assert coverage([(0, 4)]) == 5


def test_coverage_wide():
    assert coverage([(0, 9)]) == 10


def test_coverage_empty():
    assert coverage([]) == 0


def test_coverage_of_plan():
    assert coverage(plan(10, 5)) == 10


def test_coverage_overlapping_counts_once():
    assert coverage([(0, 4), (2, 6)]) == 7


def test_coverage_duplicate_slice_counts_once():
    assert coverage([(0, 4), (0, 4)]) == 5


def test_coverage_touching_slices():
    assert coverage([(0, 3), (4, 9)]) == 10
