"""分层配置合并。"""

from __future__ import annotations

from pipekit import deep_merge


def test_merge_flat():
    assert deep_merge({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}


def test_merge_override_scalar():
    assert deep_merge({"a": 1}, {"a": 2}) == {"a": 2}


def test_merge_nested():
    assert deep_merge({"b": {"x": 1}}, {"b": {"y": 2}}) == {"b": {"x": 1, "y": 2}}


def test_merge_nested_override():
    assert deep_merge({"b": {"x": 1, "z": 9}}, {"b": {"z": 2}}) == {"b": {"x": 1, "z": 2}}


def test_merge_empty_base():
    assert deep_merge({}, {"a": 1}) == {"a": 1}


def test_merge_empty_override():
    assert deep_merge({"a": 1}, {}) == {"a": 1}
