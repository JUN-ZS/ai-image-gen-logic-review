# SS.验.PAD大 · 根冻结 + 沙盒 MOD · write 01616

## 问题
不想因每个 PROJECT 调 pad 而改「根程序」预设。

## 解
```
根 CONSTITUTION_SS_YAN_PAD_DA_ROOT/defaults/   ← 永不被 run 改
        │
        │  read-only load
        ▼
新 PROJECT/sandbox/MOD.json                   ← 外挂微调（可改）
        │
        │  deep_merge(allowed only)
        ▼
effective（仅本项目）→ S0–S11 跑
```

## 金句
1. **根 PAD 加大预设铺好即锁**；项目只碰沙盒。
2. **沙盒-(X) = MOD 外挂**，类似游戏 MOD，卸掉即回根。
3. 禁路径（洞外0、冻座、四态链、勤力）**沙盒改不了**。

## 新项目模板
```
SETS/PROJ_xxx/
  sandbox/
    MOD.json          # 只写要动的键
    MOD_META.json
  Bus/ ...
  L/ ...
```

## 加载伪码
```python
root = load(ROOT/defaults/PAD_DA_DEFAULTS.json)
mod  = load(PROJECT/sandbox/MOD.json)  # 可缺省 = {}
eff  = deep_merge_allowed(root, mod, schema)
assert root 未被写回
```
