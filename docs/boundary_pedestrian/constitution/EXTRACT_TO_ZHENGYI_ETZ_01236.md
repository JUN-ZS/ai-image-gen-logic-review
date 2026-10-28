# §0.12.36 抽衣就正循環（EXTRACT→正 · ETZ）

> asof 2026-10-29 HKT  
> **用戶：**「不,是那抽衣出來就正的循環試反.推憲」  
> **正名：抽衣就正循環** · **碼 ETZ** · Extract-To-Zhengyi  
> **地位：** **LOCK** · 正衣先行 ZYF §0.12.35 之上游 **製板循環**  
> **一句：** 從全幅 **抽出衣語 → 洗到對稱／材質正 → 鎖成正衣板 → 再合**；合失敗則 **反推哪環斷**，不在全圖 Soft 硬修。

---

## 1. 循環圖（不可跳）

```
[BASE 全幅 native · 姿/人/杖]
        │
        ▼
  E0  抽衣 EXTRACT
      · 自 BASE 裁甲 ROI 或 自圖找衣語板
      · 或 世界 READ 後一次空衣產品板
      · 產物：DRAFT_GARM · role≠BASE
        │
        ▼
  E1  就正 CORRECT（可多輪 · 有閘）
      · 對稱趨勢 donor（L/R 加劇板）
      · flipavg 種子 · GEN hybrid 解鬼影
      · L0 場 + N2R cand 洗 FREE 噪
      · ncc 對稱 / 目視 hex 格界
      · 產物：正衣 LOCK · role=zhengyi_lock
        │
        ▼
  E2  合新 WEAR（S1 / GOU / MSR-L5）
      · asset[0]=BASE 姿主 · asset[1]=正衣
      · 或 GOU densify(crop, 正衣)→ECC→V5
      · 臉：FACE_OVAL 貼 BASE 或 α≈0（禁軟臉病毒）
      · 杖：OTL0 Verify
        │
        ▼
  E3  反推 DIAG（合失敗才走）
      · 臉毒／重影 → 非重雕衣 · 貼 BASE 臉
      · 網糊 < 正衣 → ROI densify only · 臉 α=0
      · 衣拓歪 → 回 E1 重就正 · 禁合時改拓
      · 姿漂 → 回 E2 · asset[0] 必須有人全幅
      · 正衣當 [0] 開新構 → 憲禁 · 重排
        │
        └──────── 可再 E0/E1 收細 ────────┘
```

**與 ZYF 差：** ZYF 說「先正衣再合」；**ETZ 說正衣從哪來、怎麼洗正、合壞怎麼反**。

---

## 2. 試錯年表（本鏈反推 · 入憲）

| 序 | 試 | 症 | 根因 | 解救 → 憲位 |
|----|-----|-----|------|-------------|
| 1 | 全圖 Soft 求對稱 | 2D 高 · 3D 律動錯 | 未抽衣 | **E0 先抽** |
| 2 | 正衣當 asset[0] 開新構 | 姿漂 | 空衣當姿主 | **[0]=有人 BASE** |
| 3 | 只 V5/貼皮當換衣 | 衣語不真 | 無 GEN densify | S1 或 GOU T3 |
| 4 | GOU fill 過肥 | 邊界糊 | 未勾形 | T7 shape · fill 0.45–0.65 |
| 5 | 密網 V5 後臉軟／亮漂 | **臉病毒** | 臉進了 GEN/V5 | **貼 BASE 臉 · α_face=0** |
| 6 | 合後網 < 正衣 090a 清 | 透視+再採樣 | 全幅稀釋 HF | **ROI 密網追清 · 不重全圖** |
| 7 | flipavg 鬼影 | 硬 L/R | 背景干擾 | GEN hybrid resolve |
| 8 | 對稱板 090a 成 | ncc↑ · 空衣正 | **E1 就正成功** | role=lock |
| 9 | S1 同姿換衣 ~90% | 姿對 · 衣語入 | 語意鎖非像素貼 | **S1 合路徑** |
| 10 | 貼臉+正衣再合 | 臉 ncc→1 | E3 臉閘 | FACE_PASTE |

**用戶鎖句：**  
「不,是那抽衣出來就正的循環試反.推憲」  
→ 製板循環 **ETZ** 與合新分離；反推以環為單位，不治標改全圖。

---

## 3. 正名與鄰條

| 欄 | 值 |
|----|-----|
| **正名** | **抽衣就正循環** |
| 碼 | **ETZ** · Extract-To-Zhengyi |
| 條 | **§0.12.36** |
| 上游產物 | **正衣 LOCK** → 喂 ZYF L2′ / MSR L2′ |
| 下游合 | S1 同姿換衣 · GOU T2–T10 · MSR L4–L5 |
| 鄰 | ZYF §0.12.35 · MSR · N2R/WNK · OTL0 · FACE 貼 · VIRUS §0.12.23 |

---

## 4. 一刀參數卡

```
MODE=ETZ
BASE_ASSET=          # 全幅有人
E0_EXTRACT= crop_armor | self_find_plate | world_once_empty
E1_CORRECT= flipavg+GEN | N2R_wash | trend_donors
E1_PROOF= bilateral_ok · hex_clear · role=zhengyi_lock
E2_WEAR= S1 | GOU | MSR_V5
FACE= paste_BASE | alpha0
WEAPON= OTL0
ON_FAIL= E3_DIAG → 回 E1 或 ROI densify · 禁全圖 Soft
```

---

## 5. PROOF 閘

| 環 | 過線 |
|----|------|
| E0 | DRAFT 非 BASE · 有衣語 |
| E1 | 正衣目視對稱 · 格界清 · META role=zhengyi_lock |
| E2 | 同姿可辨 · 衣語入 · 杖不崩 |
| 臉 | face_ncc vs BASE 高 **或** 像素貼後 ≈1 · 無重影軟臉 |
| 網 | 若追正衣清 → ROI densify ncc≥0.75 · 臉 α=0 |

---

## 6. 禁

| 禁 | 改 |
|----|-----|
| 未抽衣就全圖修對稱 | E0→E1 |
| 正衣當 BASE / 當姿主 | role=lock only |
| 合時重雕衣拓 | 回 E1 |
| densify 帶臉進 V5 | 臉貼 / α=0 |
| 治標只改一幀不返環 | E3 點名環 |

*END §0.12.36 抽衣就正循環 ETZ*

## 連動 · E2 掃毒
合身寫入若舊甲鎖死 donor → 走 **§0.12.37 SCD 衣槽清掃毒**（睡衣清槽→再寫正衣）。
