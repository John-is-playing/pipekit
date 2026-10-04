# pipekit

一个刻意设计的**小型分片流水线 / 区间计算库**，用来真实验证 Fissue 的完整链路：

抓取 → AI 评测 → 生成验证器 → 沙盒 F2P 验证 → 自动修复提 PR。

## 为什么是「又一个库」

演示用的 GitHub 仓库不应只有一两个。`pipekit` 与前两套夹具完全独立：

| 夹具 | 领域 | 特点 |
|---|---|---|
| `textkit` | 文本处理 | 单模块、独立函数 |
| `ratekit` | 金额 / 费率 | 单模块、数值边界 |
| **`pipekit`** | **分片流水线 / 区间** | **多模块、调用链耦合** |

它回答一个更硬的问题——**当 bug 藏在跨模块的调用链上，Fissue 还能不能
定位到正确的文件、写出能真正复现的验证器、并且不把别处改坏？**

## 模块与依赖关系

```
config.py      分层配置合并（默认值 + 仓库覆盖）
resolver.py    逻辑引用 → 本地对象（索引解析）
intervals.py   闭区间：相交 / 合并
slices.py      分页切片：相邻合并 / 取尾
filterops.py   按区间过滤数据点
pipeline.py    分片流水线：plan / drop_ranges / coverage
stats.py       统计辅助（只读消费 pipeline 的结果）
```

调用链（耦合点）：

```
pipeline.coverage  ──► intervals.merge
pipeline.drop_ranges ─► filterops.in_ranges
stats.count_batches ──► pipeline.drop_ranges
slices.merge_adjacent ─► (与 intervals 同口径的闭区间语义)
```

同一个语义约定（**闭区间、端点相接即视为相邻/相交**）散落在
`intervals`、`slices`、`filterops` 三处。任何一处口径写歪，
都会在 `pipeline` / `stats` 的链路上放大成可观测的错误。

## 公开 API

| 函数 | 说明 |
|---|---|
| `intervals.normalize(start, end)` | 校验并规范化一个闭区间 |
| `intervals.overlaps(a, b)` | 两个闭区间是否相交（含端点相接） |
| `intervals.merge(intervals)` | 合并全部相交/相接区间 |
| `slices.normalize_slice(start, end)` | 校验并规范化一个切片 |
| `slices.merge_adjacent(slices)` | 合并相邻或重叠的切片 |
| `slices.slice_tail(items, n)` | 取末尾 n 个元素 |
| `filterops.in_ranges(point, ranges)` | 点是否落在任一闭区间内 |
| `filterops.exclude_ranges(points, ranges)` | 剔除落在区间内的点 |
| `pipeline.plan(total, size)` | 把 `[0, total)` 切成闭区间分片 |
| `pipeline.drop_ranges(slices, ranges)` | 从分片中剔除落在 ranges 内的分片 |
| `pipeline.coverage(slices)` | 分片覆盖的总点数（重叠只算一次） |
| `resolver.resolve_index(items, index)` | 取第 index 个元素，越界抛 IndexError |
| `config.deep_merge(base, override)` | 深度合并，返回新字典（不改入参） |
| `stats.count_batches(slices, ranges)` | 剔除 ranges 后剩余分片数 |
| `stats.batch_bounds(slices, ranges)` | 剔除后分片的起止范围 |

## 本地自检

```bash
cd demo/pipekit/repo
python -m pytest -q            # 基线应全绿
```

> 基线测试**刻意不覆盖**那些有问题路径——缺陷藏在没被覆盖的边界上，
> 逼 Fissue 真正去「读代码 → 写验证器 → 跑 F2P」，而不是抄现成测试。
