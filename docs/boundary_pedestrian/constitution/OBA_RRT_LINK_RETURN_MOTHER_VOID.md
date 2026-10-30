# OBA × RRT 聯動鐵序 · 回母 VOID
# §0.12.44.**O** + §0.12.46 嵌接 · asof 2026-10-30T18:54:59Z

> **正名：** 一人累貼 × 殘相轉生 · **回母 VOID**  
> **金樣 refs：**  
> - `66a6568a` STEP 三格 peep｜HD｜**VOID 累貼**  
> - `eadb9176` 母 + 黃 GRID 座標 + 字母人  
> - `1e3908c0` 母 peep 彩圖（形真源）  
> - `f168a1ba` 母／VOID 同 GRID · peep 綠描鎖位  
> **用戶鐵句：** 入憲技「一人累貼」→ 這些圖的做法要**聯動「殘相轉生」**，並順理出**正確次序去回到母圖 VOID**

---

## 0. 一句

**母只供位／形／光** → 抽出 peep → **殘相轉生 1→2→3→1A** → **只在母 VOID 上空台** 遠→近一次一件貼 1A → STEP 線對看 → 全齊＝**在 VOID 上重建母位形**（禁貼回母圖本體）。

```
母圖 ──SCAN──▶ peep/REF ──RRT──▶ 1A ──OBA──▶ 母VOID 累貼 ──▶ FINAL
                  │                        ▲
                  └──── 量尺 peep s≤1 ──────┘
```

---

## 1. 金樣三格＝聯動視覺憲法

| 格 | 金樣 66a6568a | 聯動後 |
|----|---------------|--------|
| 左 | 綠描 peep | **VER.1** 殘相 · 母原本動作 |
| 中 | HD solo | **VER.1A**（經 2 生全形 → 3 反補 · 動作不變） |
| 右 | **VOID 上累貼** | 母 VOID + 已貼件 + 本件 1A |

**線對看：** 左 peep 邊 vs 中 1A 姿 · 中 1A 邊 vs 右 paste 位。

---

## 2. 正確全序（不可顛倒 · 回母 VOID）

```
════════════════════════════════════════
 PHASE-0  母台（只讀 · 禁當貼底）
════════════════════════════════════════
P0.1  選定最新母圖 asset · 全鏈只此母
P0.2  母圖登記 · size · IC 光

════════════════════════════════════════
 PHASE-1  回母 VOID（空台 · 最終唯一貼底）
════════════════════════════════════════
P1.1  母圖 VOID = 重 PROMPT 無人／無物 · 同幅同光 · cover_fit 母
P1.2  VOID 繼承黃 GRID 座標（與母同格）
P1.3  **禁** 母圖當 accum 底（E-OBA-03）
P1.4  accum0 = VOID  · 路徑 00_VOID.jpg

→ 這就是「回到母圖 VOID」：之後所有 paste **只准落在此 VOID**

════════════════════════════════════════
 PHASE-2  格人脫鉤 + peep 量尺（SCAN）
════════════════════════════════════════
P2.1  黃 GRID on 母 + on VOID · 格號 1..N = **座標 only**
P2.2  人／機 字母 A.. · **≠ 格號**（§0.12.44.K）
P2.3  peep mask（母 RGB · Voronoi 互斥 · 綠 2px stroke）
P2.4  peep 量尺：peep_w/h · foot · cx · **s 源只 peep**
P2.5  遠→近序 = peep_foot_y asc
P2.6  彩 peep map · REGISTRY（grid_id=null）

════════════════════════════════════════
 PHASE-3  每件殘相轉生（§0.12.46 · 先於貼）
════════════════════════════════════════
for L in far→near:          # 仍未貼 · 只產 cut
  P3.1  VER.1 = 綠 peep REF 原本動作     # 金樣左格
  P3.2  VER.2 = 生全形 ASC FROM 1        # 中間 · 禁貼
  P3.3  VER.3 = 反補（body←2 · action_lock←1）
  P3.4  VER.1A = 1 之無擋同動作 cut      # 金樣中格 · 唯一合法 cut
  P3.5  hard α 退地 · peep 量 s≤1 預算

════════════════════════════════════════
 PHASE-4  一人累貼 on 母 VOID（§0.12.44.M）
════════════════════════════════════════
accum = 母VOID
for L in far→near:
  P4.1  cut = VER.1A only                # 禁 VER.2 · E-RRT-01
  P4.2  s = min(peep_h/cut_h, peep_w/cut_w, 1.0)
  P4.3  腳錨 peep_foot + peep_cx · 貼入 **accum（VOID 系）**
  P4.4  存 accum/NN_AFTER_L.jpg
  P4.5  STEP 三／四格線對看：
        [VER.1 peep] | [VER.1A] | [accum on VOID]
        （可加 VER.2 MID 格）
  P4.6  過閘 → 下一件 · fail 只重該件鏈

════════════════════════════════════════
 PHASE-5  回母核對
════════════════════════════════════════
P5.1  FINAL = 全件貼完之 VOID 累積
P5.2  半透 綠 peep vs 紅 paste · 母 GRID+字母
P5.3  mean|mother−FINAL| 或 peep recall 自審
P5.4  **形在 VOID 上重建母位** · 非母像素底
```

---

## 3. 「回母 VOID」定義（寫死）

| 是 | 否 |
|----|-----|
| 貼底 = **從母派生的 VOID 空台** | 貼底 = 母圖本體（E-OBA-03） |
| VOID 同母幅／光／GRID 座標 | VOID 隨便空板（E-OBA-20） |
| FINAL 站在 VOID 上重現母位形 | 在母上 inpaint 留人 |
| 每步 accum 右格 = VOID+已貼 | 右格 = 母+貼 |

**金樣右格永遠係 VOID 累積** · 唔係母圖。

---

## 4. 聯動關係圖

```
        §0.12.44 一人累貼 OBA              §0.12.46 殘相轉生 RRT
        ─────────────────                 ─────────────────
        格人脫鉤 · peep 量尺                 1→2→3→1A
        一次一件 · 線對看                    只交 1A
        遠→近 · 腳錨                        動作鎖 1
                 \                         /
                  \    聯動 .O            /
                   v                     v
              ┌─────────────────────────────┐
              │  母 VOID = 唯一 accum 底     │
              │  paste = 1A only · s=peep   │
              │  STEP = 1 | 1A | VOID+accum │
              └─────────────────────────────┘
```

---

## 5. 一刀參數卡（聯動）

```
MODE=OBA_x_RRT_RETURN_MOTHER_VOID
PHASE0=mother_readonly
PHASE1=VOID_from_mother  accum0=VOID  BAN mother_as_base
PHASE2=GRID_coords_only + letters + peep_ruler
PHASE3=RRT 1→2→3→1A per_unit  BEFORE_paste
PHASE4=paste_1A_on_VOID one_by_one STEP_audit
PHASE5=mother_bite_check on_VOID_final
STEP_COLS=VER1_peep | VER1A | accum_on_VOID
BAN=paste_on_mother, paste_ver2, batch, grid_scale, free_studio, skip_void
GOLD=66a6568a,eadb9176,1e3908c0,f168a1ba
```

---

## 6. 錯成（聯動）

| 碼 | 禁 |
|----|-----|
| **E-OBA-03** | 母圖當貼底 · 唔回 VOID |
| **E-OBA-20** | VOID 非母派生 |
| **E-RRT-01** | 貼 VER.2 · 跳 1A |
| **E-OBA-26** | batch 貼 · 無逐步 VOID 右格 |
| **E-LINK-01** | 有 RRT 無 OBA 序 · 1A 亂貼非 VOID |
| **E-LINK-02** | 有 OBA 無 RRT · 棚拍 HD 當中格（脫離 1 動作） |
| **E-LINK-03** | STEP 右格用母圖而非 VOID 累積 |

---

## 7. 與金樣逐步對照

| 金樣 | 聯動步 |
|------|--------|
| f168 母+VOID 雙 GRID · peep 綠 | P1–P2 |
| eadb 字母≠格號 | P2.1–P2.2 |
| 1e3908 彩 peep 形源 | P2.3–P2.6 |
| 66a6568a STEP1..N | P3+P4 每件 |

---

## 8. 檔位

| | |
|--|--|
| 本節 | `OBA_RRT_LINK_RETURN_MOTHER_VOID.md` |
| 主憲嵌 | §0.12.44.**O** · §0.12.46 連動 |
| 金樣 | minifig `66a6568a` 等 |

---

*END · OBA×RRT 聯動 · 回母 VOID · asof 2026-10-30T18:54:59Z*
