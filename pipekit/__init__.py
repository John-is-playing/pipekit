"""pipekit —— 一个用于演示 Fissue 的小型分片流水线 / 区间计算库。

模块分工：
    intervals   闭区间：相交 / 合并
    slices      分页切片：相邻合并 / 取尾
    filterops   按区间过滤数据点
    pipeline    分片流水线：plan / drop_ranges / coverage
    resolver    逻辑引用 → 本地对象
    config      分层配置深度合并
    stats       统计辅助（只读消费 pipeline 的结果）
"""

from . import config, filterops, intervals, pipeline, resolver, slices, stats
from .config import deep_merge
from .filterops import exclude_ranges, in_ranges
from .intervals import merge, normalize, overlaps
from .pipeline import coverage, drop_ranges, plan
from .resolver import resolve_index
from .slices import merge_adjacent, normalize_slice, slice_tail
from .stats import batch_bounds, count_batches

__version__ = "0.3.1"

__all__ = [
    "config",
    "filterops",
    "intervals",
    "pipeline",
    "resolver",
    "slices",
    "stats",
    "deep_merge",
    "exclude_ranges",
    "in_ranges",
    "merge",
    "normalize",
    "overlaps",
    "coverage",
    "drop_ranges",
    "plan",
    "resolve_index",
    "merge_adjacent",
    "normalize_slice",
    "slice_tail",
    "batch_bounds",
    "count_batches",
    "__version__",
]
