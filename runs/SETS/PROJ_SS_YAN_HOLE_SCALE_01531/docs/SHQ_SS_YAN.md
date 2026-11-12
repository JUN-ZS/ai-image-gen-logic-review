# SS驗

{
  "write_id": "01531",
  "formal": "SHQ_SS_YAN_SX_VERIFY_V1",
  "zh": "SS驗",
  "call": "SS驗",
  "stick": "STICK_SS_YAN",
  "equation": "SS驗 = ∀(Si,Sj) ∈ 同域： size_lock ∧ (有洞⇒ outside(Si,Sj,M)=0) ∧ 跨域⇒必須 map/S(X)A/hardpaste",
  "from": [
    "01530 遠景三物對位診斷",
    "01528 S(X)A",
    "01503 S11×S0",
    "框牙"
  ],
  "purpose": "把 (S)×(S) 對位驗收立為憲技：先驗域、再驗尺、再驗洞外、再驗四態落點",
  "gates": {
    "G0_DOMAIN": "同域才可比；跨域未 map = FAIL_CROSS_DOMAIN",
    "G1_SIZE": "同域 size_lock",
    "G2_OUTSIDE": "有 MARK 時洞外 max_diff=0",
    "G3_RATIO": "S5 peep aspect vs MARK bbox aspect err≤tol",
    "G4_ELEV": "S7 elev 尺 = peep；elev≠S11/RETURN",
    "G5_S11xS0": "S01/S11 回母幀洞外0",
    "G6_ALGEBRA": "除洞扣生反 落點 S 可追溯"
  },
  "domains": {
    "母幀": [
      "S0",
      "S01",
      "L1_full"
    ],
    "工域S0A": [
      "S0A",
      "S1_work",
      "S3",
      "S9",
      "S10",
      "S11_work"
    ],
    "peep": [
      "S5",
      "S7",
      "S7A",
      "S9A_peep"
    ],
    "放大暫態": [
      "S6",
      "S(X)A densify 中間"
    ]
  },
  "error_codes": {
    "E-SS-00": "跨域直接比",
    "E-SS-01": "同域 size mismatch",
    "E-SS-02": "洞外 ≠0",
    "E-SS-03": "peep RATIO vs 洞",
    "E-SS-04": "elev≠peep 或 elev 冒 RETURN",
    "E-SS-05": "S11/S01 未鎖 S0",
    "E-SS-06": "除輸入尺 ≠ S0（如 L1 2×）",
    "E-SS-07": "S6 放大未回鎖 peep 即當 peep"
  },
  "ACCEPT_FULL_HD": false
}
