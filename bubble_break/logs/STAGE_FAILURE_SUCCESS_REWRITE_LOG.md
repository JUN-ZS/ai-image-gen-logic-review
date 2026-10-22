# 雙頭圓柱槌・泡泡種植式 — 階段失敗／成功／改寫 LOG

> Repo: `JUN-ZS/ai-image-gen-logic-review`  
> Branch journey: `feat/dense-hammer-bubble-pick` → **main**  
> Date range: 2026-10-21  
> Formula base: \(D_h=0.08D_b,\ H_h=1.5D_h,\ L_g=3H_h,\ D_g=D_h/10\)

**Purpose:** every stage records **FAIL causes → rewrite → PASS criteria → asset/commit anchors**, so the next stage inherits locks instead of freehand wipe.

---

## Global hard locks (accumulated)

| Lock | Meaning | Proven when violated |
|------|---------|----------------------|
| **Planted cylinder** | Double-ended cylinder along bubble normal; not flying spike | Early wrong “槌朝泡泡撞” framing |
| **Base glow contact** | Glow only at conformal base–shell interface | Outer-end glow = wrong |
| **Side-middle handle @90°** | Handle from cylinder side mid; not base, not axial extension | Outer-end new shaft = FAIL |
| **NO_NEW_HANDLE** | Cannot invent second rod / outer-end shaft | Stage C/D skips |
| **Person∶Hammer = 1∶1 mini** | Full-body visual area ≈ hammer area | Life-size person = FAIL |
| **B3 master topology** | `80c3e341` freezes hammer geometry | Any stage without B3 drift |
| **PROVEN left-handle rule** | 跳過「握既有左柄」會長新柄；鎖左柄像素後可壓住 | D2 outer-end grip attempts |
| **Step chain** | D0→D1→D2→D3→D4 only; no skip | Skipping D1/D2 grows new handle |
| **Full program RUN** | Each step re-runs compiler + gates | “寫死” without RUN still fails |
| **Serial full-frame wash** | Multi-pose = N× full IMG→IMG, never 1-image 20-grid gen | Control sheet unlocks topology |
| **Script gates + human audit** | `outer_end_empty` + `side_handle_present`; metal FO false fail → human wins | D3 outer heuristic |

Key commits (feat → main):
- `e4219fd` — proven left-handle hard lock  
- `52f68e2` — D3 control sheet helper (later diagnosed: gen-board ≠ lock)  
- `cb1031b` — stage_d_gates step_chain + pixel gates  

---

## Stage A — Dense candidates (24 planted hammers)

### Intent
Dense planting of same-ratio double-ended cylinders on one bubble; base glow; lateral handles; **no person**.

### FAIL / near-miss
| Issue | Cause | Rewrite |
|-------|-------|---------|
| Conceptual “flying hammer into bubble” | Prompt framed impact as subject | Rewrite geometry: plant like trees, radial normals |
| Labels / pick confusion (C08 on wrong atlas) | User picked non-existent label | Clarify atlas → **C13** |

### PASS
- Stage A rasters generated; C13 selected for isolation.  
- Anchors: dense atlas assets (e.g. `46294bd9…`, later denser runs).

### Handoff to B
**Must use real Stage A raster** as image reference; do not re-text-invent the hammer.

---

## Stage B — Isolate one hammer (C13) + topology repair

### Intent
Keep one C13; remove other 23; preserve base, glow interface, side handle joint.

### FAIL
| Issue | Cause | Rewrite |
|-------|-------|---------|
| Weak / missing lateral handle after isolation | Isolation loses thin side rod | **Region zoom 4×** on cylinder (`不接受,你把那柱做區域放大`) |
| Handle axis rewritten to axial | Model defaults to sledgehammer | Explicit REJECT of axial rewrite; multi-axis candidates |
| Early picks wrong axis | Some candidates OK different axes, one FAIL | User: “這圖柄改軸向, 這是不應出的錯” |

### PASS — B3 master
| Asset | Note |
|-------|------|
| **`80c3e341-0af7-43d8-97c7-11dbdaac2d40`** | Correct XYZ cross at cylinder axis; side handle mid; outer empty; base glow |

### Why B3 “做對”
Correct **radial cylinder axis × lateral handle at side-middle cross**; full base contact; not freehand guess after zoom+reference lock.

### Handoff to C/D
**B3 is frozen topology mother.** No later stage may redesign hammer; only person/action/FX around it.

---

## Stage C — Scale + person (superseded into D)

### Intent (original)
Scale bubble/hammer; add holder; person must not deform hammer.

### FAIL
| Issue | Cause | Rewrite |
|-------|-------|---------|
| New handle appears despite B3 | Model adds grip-friendly shaft at outer end | Hard: **不能加柄** |
| Life-size person | Misread 1∶1 as same height | **1∶1 = mini** body area ≈ hammer area |
| Premature “correct 气势” demand | C was scale+presence only | Split: presence vs action → **open Stage D** |

### PASS criteria rewritten
C/D0–D1 only: mini “她” near locked hammer, **no first grip yet** if grip causes new handle.

### Handoff
User: 開 D — 找持槌氣勢＋動作，從 B3 重構；一步步；外端新柄不可能在層層公式中出現。

---

## Stage D micro-steps

### D0 — Topology freeze
- Source: B3.  
- PASS: packet freeze text + step chain lock.

### D1 — Mini person, no grip
| | |
|--|--|
| Asset | `75f64e33-4840-4ea3-8dcb-3b089de4a786` |
| PASS | Mini 她; outer empty; side handle present; no grip |
| Person ref | `6ee74baf…`（她） |

### D2 — First grip on **existing left** side handle only
| FAIL attempts | Cause | Rewrite |
|---------------|-------|---------|
| Outer-end grip / new stub | Skip left-rod pixel lock | **PROVEN rule** + `FIRST_GRIP_STEP=D2` + prev raster SHA lock |
| Jump D1→grip | Skip step_chain | Gates reject illegal transition |

| PASS | Asset |
|------|-------|
| Left continuous rod grip, outer empty | **`db0f7849-ac31-4802-a8a9-f7d5fdcaa161`** |

**Proven statement (law):**  
> 跳過「握既有左柄」會長新柄；鎖左柄像素後可壓住。

### D3 — 找／持槌 tension + action wash
| Approach | Result | Rewrite |
|----------|--------|---------|
| Single full-frame IMG→IMG from D2 | PASS (e.g. `a7cd0f48` full back) | Keep serial full-frame |
| 20-cell ControlNet mother board in **one** gen | Topology unlocks (cell 03 bare hammer, renumber chaos) | **Root cause:** 1 image / 20 tasks / ~5% px per cell = no pixel lock |
| Serial wash 6 mixed poses | Script 6/6 outer+side; human OK | Prefer this for multi-combo |
| Serial wash 6 **back-only** from D2 | Many face-front / flipped cylinder / free rod | Full-back force re-layouts scene → use proven back as source |

| PASS D3 master (user pick) | Asset |
|----------------------------|-------|
| B6 full back + left rod | **`e8310236-8fa7-41ea-964a-b47cf8b80787`** |
| Prior back PASS (ref) | `a7cd0f48-3307-45bb-92fe-9677a6bb3a28` |

**Diagnosis log (multi vs single):**  
- Single: full bandwidth + one edit + D2 pixels → lock holds.  
- Multi-grid gen: parallel collage, gate on whole board, not per-cell → **lock dies**.  
- Correct multi: **serial N full frames**, optional montage for display only.

### D4
Optional polish; user advanced to Stage E from locked D3 without long D4 dwell.

### Handoff to E
D3 locked = B6; FX must not rewrite handle.

---

## Stage E — Glow / cracks / shatter

### Intent
Expand glow from base contact → shell cracks → shockwave / break. Still planted; left grip; outer empty.

### PASS (user mid-frame)
| | Asset | Note |
|--|-------|------|
| **E1 mid (impact)** | **`23fc19cf-37dd-4fd5-a36a-4a955f1434d8`** | Shock rings + shards; locks hold |
| E2 heavy cracks | `e9558022-6f98-4f1f-a654-c828cf26a7be` | Stronger shell cracks |

### Trilogy rewrite (pre / mid / end)
User: mid = E1; need **pre (蓄力, intact)** + **end (epic blast)** with protocol wisdom.

| Frame | Asset | FAIL notes | PASS notes |
|-------|-------|------------|------------|
| PRE close contact | `0197a559…` | Too close for “遠距” | Intact bubble, left rod |
| PRE “far” wrong topo | `492e882c…` | Long axial sledge | Distance OK |
| PRE inside bubble | `1082a1ce…`, `ce203d1e…` | Not outside gap | — |
| PRE far + side-ish | **`808b7b97…`** | Vertical barrel variant | **Gap + no contact** recommended earlier |
| PRE L-handle | `2b69ba9f…` | Topology FAIL | Discard |
| MID | `23fc19cf…` | — | User locked |
| END | **`3d5629a1…`** | — | Epic shatter |
| END alt | `0b373308…` | Silhouette | More violent |

**Rewrite for “拉力更遠於泡”:** spacing is a **time-axis** constraint, not only FX; far pre often fights side-handle lock → prefer sources that already pass distance+side, or accept distance PASS / topo PARTIAL and document.

### Continuous video
| | |
|--|--|
| Asset | **`a073edd6-7d5e-4226-8161-0264f6f6e76f`** (10s) |
| Keyframes | 492e (0) → 1082 (2) → e831 (4.5) → 3d56 (7) → 0b37 (10) |
| Note | Opening inherits long-handle pre; mid/end closer to locked cylinder+side rod |

---

## Stage chain summary (success path)

```text
A dense plant → pick C13
  → B isolate + zoom repair → B3 master 80c3e341
  → D0 freeze
  → D1 mini 她 no-grip 75f64e33
  → D2 first grip LEFT rod db0f7849   [PROVEN lock]
  → D3 serial full-frame action → B6 e8310236
  → E mid 23fc19cf
  → PRE/END trilogy + video a073edd6
```

---

## Failure taxonomy (for future stages)

1. **Geometry default bias** — sledge axial shaft / flying spike.  
2. **Isolation loss** — thin lateral rod disappears without ROI zoom.  
3. **Scale semantic error** — 1∶1 read as life-size.  
4. **Grip invention** — new outer handle when left rod not pixel-locked.  
5. **Step skip** — D1/D2 skipped → same as (4).  
6. **Bandwidth split** — multi-cell one-shot gen destroys locks.  
7. **Pose force re-layout** — “must full-back” re-solves whole scene, flips hammer.  
8. **Time-axis distance** — “far from bubble” fights planted contact continuity.  
9. **Gate false positive** — outer_end_empty on metal body → always pair human audit.

---

## Code / docs touched (feat, merge to main with this log)

| Path | Role |
|------|------|
| `bubble_break/DENSE_HAMMER_BUBBLE_SELECTION_WORKFLOW.md` | Stage table + proven locks + control-sheet note |
| `bubble_break/dense_hammer_bubble_workflow.py` | Packet compiler, D steps, control sheet helper |
| `bubble_break/stage_d_gates.py` | step_chain, outer/side gates, PROVEN_RULE |
| `bubble_break/test_dense_hammer_bubble_workflow.py` | Unit tests (19+) |
| `bubble_break/logs/STAGE_FAILURE_SUCCESS_REWRITE_LOG.md` | **This file** |

---

## Asset index (anchors)

| Role | UUID |
|------|------|
| B3 topology master | `80c3e341-0af7-43d8-97c7-11dbdaac2d40` |
| 她 person ref | `6ee74baf-2c16-44e8-aa14-b771002c7ebd` |
| D1 mini no-grip | `75f64e33-4840-4ea3-8dcb-3b089de4a786` |
| D2 left grip | `db0f7849-ac31-4802-a8a9-f7d5fdcaa161` |
| D3 B6 back | `e8310236-8fa7-41ea-964a-b47cf8b80787` |
| D3 back ref | `a7cd0f48-3307-45bb-92fe-9677a6bb3a28` |
| E1 mid | `23fc19cf-37dd-4fd5-a36a-4a955f1434d8` |
| E2 | `e9558022-6f98-4f1f-a654-c828cf26a7be` |
| PRE far side-ish | `808b7b97-61ce-4a90-a66f-a4a4bab9616d` |
| PRE far sledge (distance only) | `492e882c-96bc-46f7-8981-9ad3503b6cd4` |
| PRE near | `1082a1ce-34c9-4d98-a0fb-bae0a83d9249` |
| END | `3d5629a1-0672-44a2-beea-6a308245a71c` |
| END alt | `0b373308-2823-4350-b9d2-3297ac6bba7a` |
| Video 10s | `a073edd6-7d5e-4226-8161-0264f6f6e76f` |

---

## Next-stage rule (from this log)

1. Full program RUN every step.  
2. Inherit previous **PASS asset SHA**, not free text.  
3. One full-frame edit per step; multi-combo = serial only.  
4. Gates + human; FAIL → rollback, do not push forward.  
5. Append this log when a new FAIL→rewrite→PASS is proven.

*End of log — 2026-10-21*

---

## H9 — Imagine track opened (2026-10-22)

**Branch:** `feat/imagine-planted-bubble-h9-20261022`  
**Module:** `bubble_break/imagine_planted_bubble_h9.py`  
**Why:** parallel closed loop that does **not** require `GEMINI_API_KEY`; provider = Grok Imagine serial full-frame under the same planted-cylinder contract.

### FAIL avoided
- Waiting on Gemini key before iterating geometry.
- Using PR #6 import sledge/city rasters as if they were B3 topology.

### PASS / rewrite
- Reuse `STAGE_SPECS` + `GLOBAL_LOCKS` from `planted_bubble_closed_loop`.
- `compile` → agent Imagine → `ingest` (hash + strip).
- Always `code_visual_acceptance_status=NOT_VERIFIED_BY_CODE`.

### First live Imagine seed (this chat)
B `7713610c` → C `caea5cca` → D1 `de5ec90f` → D2 `9a1ef2a2` → D3 `e4352bb5` → E_MID `59381c37` → E_END `49a3e9ad`
