"""统计辅助（只读消费 pipeline）。"""

from __future__ import annotations

from pipekit import batch_bounds, count_batches


def test_count_batches_keeps_computed_ranges():
    assert count_batches([(0, 4), (5, 9)], [(6, 8)]) == 2


def test_count_batches_no_ranges():
    assert count_batches([(0, 4), (5, 9)], []) == 2


def test_count_batches_empty_slices():
    assert count_batches([], [(1, 2)]) == 0


def test_batch_bounds_keeps_computed_ranges():
    assert batch_bounds([(0, 4), (5, 9)], [(6, 8)]) == (0, 9)


def test_batch_bounds_empty_slices():
    assert batch_bounds([], [(1, 2)]) is None
