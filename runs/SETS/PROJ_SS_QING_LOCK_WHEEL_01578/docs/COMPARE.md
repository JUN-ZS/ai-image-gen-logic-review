{
  "write_id": "01578",
  "subject_image": "01577 delivery robot L0",
  "part": "WHEEL",
  "金句": [
    "whole_subject（程式）= 几何整洞策略（CV）",
    "whole subject（语义）= 只写进 prompt，仍可能漂",
    "真·整件/部件回位 = MARK/peep 金框 + SS验.清锁，不靠模型懂 preset 名"
  ],
  "methods": {
    "A_CV_wheel": {
      "who": "TUNE/几何（类似 whole_subject 缩到 PART）",
      "how": "主体下带 + 暗/边缘 CC largest-k → MARK_wheel",
      "reads_preset": false,
      "semantic": false
    },
    "B_GROK_prompt_wheel": {
      "who": "外力 GROK EDIT",
      "how": "prompt 写 remove all but wheels / densify wheels only",
      "reads_preset": false,
      "semantic": "仅 prompt 近似，可漂、可长出车身"
    },
    "C_SS_QING_LOCK_PART": {
      "who": "新技：部件清锁",
      "how": "A 的 MARK_wheel 金框 + peep + densify + B_direct hard 回 L0 · outside=0",
      "sovereignty": "框主权在 MARK/peep，不在模型理解 whole_subject 名"
    }
  }
}