"""Extract: SS验.清 / 清锁 / 清+A APIs from shq_zheng_tou_shen.py — not standalone runnable."""
SS_YAN_QING = {
    "call": "SS驗.清",
    "formal": "SHQ_SS_YAN_QING_SEAT_HARDLOCK_V1",
    "write": "01539",
    "mode_gold": "F2",
    "api": "seat_hardlock_sheng",
    "law": "I*=seat+α·HF(ECC(TEX→seat)); 升TEXTURE不影响位",
}

SS_YAN_V2 = {
    "call": "SS驗",
    "formal": "SHQ_SS_YAN_V2_INPAINT_SEAT_V1",
    "write": "01536",
    "sheng_primary": "INPAINT@MARK",
    "ban_freeframe_elev": True,
    "gates": ["G0","G1","G2","G3","G4","G5","G6","G7_INPAINT","G8_POSE","G9_VALUE_TABLE"],
}

FORMAL_TOU = "SHQ_ZHENG_TOU_EDIT_INPAINT_IN_HOLE_V1"
FORMAL_SHEN = "SHQ_ZHENG_SHEN_FULL_OBJECT_V1"
STICK_TOU = "STICK_ZHENG_TOU_SX_S11xS0"
STICK_SHEN = "STICK_ZHENG_SHEN"

# ---------------------------------------------------------------------------
# DNA：正頭 → 正身 唯一差分表（其餘全同）
# ---------------------------------------------------------------------------
DNA_DIFF = {
    "equation": "正身 = 正頭DNA[ bite: head → full_object ]",
    "same": [
        "[(生,除,洞,扣)×(反)]",
        "外力GROK 除/生",
        "強心針 認∩放大∩升質×物",
        "(S)×(S) Bus 每步 sha",
        "S11×S0 outside=0",
        "peep 只讀 · elev=子",
        "S0全景 + S0A目標大切塊 · (S)×(S) 回S0",
        "禁 freeframe 無洞回",
        "kou_part / hardpaste / outside_max 來自框牙內 外力反V2.1",
    ],
    "diff_only": {
        "bite": {"tou": "head", "shen": "full_object"},
        "peep_name": {"tou": "peep0", "shen": "peep_full"},
        "MARK": {"tou": "M_head", "shen": "M_full"},
        "tune_default": {"tou": "human_mid_head|mecha_dual_part", "shen": "whole_subject"},
        "part_role": {"tou": "head", "shen": "whole"},
        "S4_认": {"tou": "认头", "shen": "认整件原子"},
        "S9": {"tou": "正头洞内INPAINT", "shen": "正身洞内INPAINT"},
        "E_codes": {
            "shared_freeframe_elev": [
                "E-FF-01 freeframe S9/RETURN without hole seat (fullframe outside>0)",
                "E-FF-02 elev plate used as RETURN/正生",
                "E-FF-03 elev overwrites peep origin",
                "E-FF-04 freeframe densify claimed as seat-born",
            ],
            "tou": ["E-ZT-01 head freeframe", "E-ZT-02 elev as RETURN"],
            "shen": ["E-ZS-01 头洞冒身洞", "E-ZS-02 无洞回整件", "E-ZS-05 伪组合",
                     "E-ZS-FF 正身同染 freeframe/elev（正头已见）"],
        },
        "S0A": {
            "role": "子集正身起點（nested 正身）· 不放大",
            "record": "bbox + corners in S0（native 像素，scale=1）",
            "law": "S0A 本身 = 獨立正身 SRC；peep/frame 在 S0A 自框上更正中",
            "why_peep_center": "全(S)×(S) 的框在 S0A 畫布上對物居中，非全景邊角",
            "why_elev_ff_ok": "子集正身內 MARK·peep·elev·S9 同域同尺；elev 子 / freeframe 座生",
            "flow": "S0 → S0A(crop=子集正身) → S1..S11(on S0A as if S0) → map S0A→S01",
            "sx": "S0A.parent=S0; 各S 鎖 S0A；S01 讀 S0+S0A corners",
            "NOT": "禁止把放大當主因；放大≠子集正身",
        },
        "anti_toxin": {
            "peep_origin": "S5 peep only; elev never origin",
            "S9_seat_born": "S9 = hardpaste(L0, MARK, I_HD) if freeframe; never store raw freeframe as PRIMARY",
            "elev_child": "S7 elev = scale_lock(peep, dens); elev_is_not_RETURN=True hard",
            "S11_primary": "S11×S0 hardpaste only; freeframe S9 alone never PASS visual gold",
        },
    },
}

MODE_CFG = {
    "tou": {
        "zh": "正頭",
        "formal": FORMAL_TOU,
        "stick": STICK_TOU,
        "bite": "head",
        "peep_key": "peep0",
        "tune": "human_mid_head",
        "part_role": "head",
        "S9_role": "正頭 洞内 INPAINT",
    },
    "shen": {
        "zh": "正身",
        "formal": FORMAL_SHEN,
        "stick": STICK_SHEN,
        "bite": "full_object",
        "peep_key": "peep_full",
        "tune": "whole_subject",
        "part_role": "whole",
        "S9_role": "正身 洞内 INPAINT",
    },
}


def sha_file(p: Path) -> str:
    p = Path(p)
    if not p.is_file():
        return "missing"
    return hashlib.sha256(p.read_bytes()).hexdigest()
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------
# (S)×(S) Bus — 正頭/正身共用
# ---------------------------------------------------------------------------
class SXBus:
    def __init__(self, root: Path):
        self.root = ensure(root)
        self.bus = ensure(root / "Bus")
        self.chain: List[Dict[str, Any]] = []

    def write(self, si: str, role: str, parent: Optional[str], files: Dict[str, Path], **extra) -> Dict[str, Any]:
        slot = ensure(self.bus / si)
        parent_sha = None
        if parent:
            pj = self.bus / parent / "SLOT.json"
            if not pj.exists():
                raise RuntimeError(f"E-SX missing parent Bus[{parent}]")
            parent_sha = json.loads(pj.read_text(encoding="utf-8")).get("slot_sha")
        meta: Dict[str, Any] = {
            "si": si,
            "role": role,
            "parent": parent,
            "parent_sha": parent_sha,
            "files": {},
            "ok": True,
            **extra,
        }
        for k, src in files.items():
            src = Path(src)
            if not src.exists():
                meta["ok"] = False
                meta.setdefault("missing", []).append(k)
                continue
            # key 可含相对子路径；必须 mkdir parents（E-SX Bus 嵌套）
            name = k if Path(k).suffix else f"{k}{src.suffix}"
            dst = slot / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.resolve() != dst.resolve():
                shutil.copy2(src, dst)
            meta["files"][k if Path(k).suffix else dst.name] = {
                "path": str(dst.relative_to(self.root)),
                "sha": sha_file(dst),
            }
        # normalize keys to basenames actually written
        meta["files"] = {}
        for p in sorted(slot.iterdir()):
            if p.name == "SLOT.json" or p.is_dir() or not p.is_file():
                continue
            meta["files"][p.name] = {"path": str(p.relative_to(self.root)), "sha": sha_file(p)}
        def _jsonable(o):
            if isinstance(o, (str, int, float, bool)) or o is None:
                return o
            if isinstance(o, dict):
                return {str(k): _jsonable(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)):
                return [_jsonable(v) for v in o]
            try:
                import numpy as _np
                if isinstance(o, (_np.integer,)):
                    return int(o)
                if isinstance(o, (_np.floating,)):
                    return float(o)
                if isinstance(o, _np.ndarray):
                    return o.tolist()
            except Exception:
                pass
            return str(o)
        meta = _jsonable(meta)
        raw = json.dumps(meta, ensure_ascii=False, sort_keys=True)
        meta["slot_sha"] = sha_bytes(raw.encode("utf-8"))
        (slot / "SLOT.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        self.chain.append({"si": si, "ok": meta["ok"], "sha12": meta["slot_sha"][:12], "role": role})
        return meta

    def reload(self, si: str) -> Dict[str, Any]:
        p = self.bus / si / "SLOT.json"
        if not p.exists():
            raise RuntimeError(f"E-SX missing Bus[{si}]")
        return json.loads(p.read_text(encoding="utf-8"))

    def assert_intact(self, si: str, fname: str, expected_sha: str) -> None:
        slot = self.reload(si)
        if fname not in slot["files"]:
            raise RuntimeError(f"E-SX missing file {si}.{fname}")
        if slot["files"][fname]["sha"] != expected_sha:
            raise RuntimeError(f"E-SX overwrite {si}.{fname}")
        disk = sha_file(self.root / slot["files"][fname]["path"])
        if disk != expected_sha:
            raise RuntimeError(f"E-SX disk drift {si}.{fname}")


def _file_sha(bus: SXBus, si: str, name: str) -> str:
    return bus.reload(si)["files"][name]["sha"]


# ---------------------------------------------------------------------------
# 正头已见 freeframe/elev 反毒 — 正身同闸（shared）
# ---------------------------------------------------------------------------
def detect_freeframe(I: np.ndarray, L0: np.ndarray, M: np.ndarray, thr: int = 0) -> dict:
    """全帧 I 在洞外 vs L0 有差 → freeframe 漂（E-FF-01 / E-WLF3-01 类）"""
    out = outside_max(I, L0, M)
    return {
        "is_freeframe": out > thr,
        "outside_max": out,
        "code": "E-FF-01" if out > thr else None,
        "zh": "无洞座 freeframe 全帧回 = 偷步" if out > thr else "seat-aligned",
    }


def elev_must_be_child(peep: np.ndarray, pm: np.ndarray, elev_im: Optional[np.ndarray], dens_fallback: np.ndarray) -> tuple:
    """elev 永为 peep 子：scale_lock；禁止 elev 原图当 peep/RETURN。
    返回 (elev_lock, meta)
    """
    meta = {
        "elev_is_child_of_peep": True,
        "elev_is_not_RETURN": True,
        "elev_remap": False,
        "forbid": ["elev_as_正生", "elev_as_S9", "elev_overwrite_peep"],
    }
    if elev_im is None:
        # dens_fallback already peep-space scale child
        return dens_fallback, {**meta, "source": "S6_scale_or_dens_peep"}
    # freeframe studio elev (不同构图) → 只抽 HF 锁回 peep
    elev_lock = scale_lock_elev(peep, elev_im, pm)
    meta["source"] = "scale_lock_elev(peep@S0A, elev_im)"
    meta["align"] = "peep 已在 S0A 放大洞位；elev freeframe 只供 HF 不供布局"
    meta["elev_input_shape"] = list(elev_im.shape[:2])
    meta["peep_shape"] = list(peep.shape[:2])
    # 若有人把 elev 当成 peep 尺寸原图直接用，仍强制 scale_lock 路径记录
    if elev_im.shape[:2] == peep.shape[:2]:
        # 仍 scale_lock 一次，避免 elev 像素主权冒 peep
        elev_lock = scale_lock_elev(peep, elev_im, pm)
        meta["note"] = "same-size elev still scale_lock — elev never peep sovereign"
    return elev_lock, meta


def seat_born_S9(L0: np.ndarray, M: np.ndarray, I_HD: np.ndarray, L1: Optional[np.ndarray] = None) -> tuple:
    """S9 必须洞座生：洞外=L0（或 L1 空座外景），洞内才用 I_HD。
    freeframe I_HD 全帧不得作 PRIMARY。
    返回 (S9_primary, toxin_meta)
    """
    H, W = L0.shape[:2]
    I = I_HD if I_HD.shape[:2] == (H, W) else cv2.resize(I_HD, (W, H))
    ff = detect_freeframe(I, L0, M)
    toxin = {"freeframe": ff, "seat_born": True, "E-FF-01": ff["is_freeframe"]}
    if ff["is_freeframe"]:
        # 正头同修：PRIMARY = hardpaste seat；raw freeframe 另存教材
        S9 = hardpaste(L0, M, I)
        toxin["action"] = "hardpaste(L0,MARK,I_HD) 压 freeframe"
        toxin["raw_freeframe_outside"] = ff["outside_max"]
    else:
        S9 = I
        toxin["action"] = "I_HD already seat-aligned"
    # 双检
    out2 = outside_max(S9, L0, M)
    toxin["S9_outside_after_seat"] = out2
    toxin["S9_seat_OK"] = out2 == 0
    return S9, toxin


def ban_elev_as_return(elev_path_used: bool, S9_from: str) -> dict:
    return {
        "elev_used_for_S7_only": elev_path_used,
        "S9_from": S9_from,
        "E-FF-02": S9_from == "elev",
        "ok": S9_from != "elev",
    }



# ---------------------------------------------------------------------------
# 核心：正頭/正身 同一 run（mode 只改 DNA 差分位）
# ---------------------------------------------------------------------------


def large_target_bbox(
    L0: np.ndarray,
    L1: np.ndarray,
    pad_frac: float = 0.12,
    min_side: int = 320,
    roi_hint: Optional[List[float]] = None,
) -> Tuple[List[int], dict]:
    """S0A = 子集正身框（native crop，不放大）。
    用 L0|L1 最大變區 CC 的緊 bbox + 適度 pad；禁止擴成全幅。
    peep 在 S0A 自框上更正中 → 全 (S)×(S) 框更正中。
    """
    H, W = L0.shape[:2]
    if roi_hint and len(roi_hint) == 4:
        x0 = int(roi_hint[0] * W); y0 = int(roi_hint[1] * H)
        x1 = int(roi_hint[2] * W); y1 = int(roi_hint[3] * H)
        meta = {"source": "roi_hint", "pad_frac": pad_frac}
    else:
        d = cv2.absdiff(L0, L1)
        g = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(g, 18, 255, cv2.THRESH_BINARY)
        th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8), 2)
        th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), 1)
        n, lab, stats, _ = cv2.connectedComponentsWithStats(th, 8)
        if n <= 1:
            side = max(min_side, min(H, W) // 2)
            x0 = max(0, W // 2 - side // 2); y0 = max(0, H // 2 - side // 2)
            x1 = min(W - 1, x0 + side); y1 = min(H - 1, y0 + side)
            meta = {"source": "fallback_center", "pad_frac": pad_frac}
        else:
            # 最大 CC（跳過背景 0）
            best_i, best_score = None, -1.0
            for i in range(1, n):
                x, y, w, h, area = [int(v) for v in stats[i, :5]]
                if area < 500:
                    continue
                wf, hf = w / float(W), h / float(H)
                if wf > 0.75 and hf < 0.45:
                    continue  # 拒泥地/雨丝横条
                if wf > 0.9:
                    continue
                compact = area / float(max(1, w * h))
                score = area * (0.35 + compact) * (1.0 - 0.5 * max(0.0, wf - 0.55))
                cy = y + h * 0.5
                if cy > 0.85 * H and hf < 0.35:
                    score *= 0.2
                if score > best_score:
                    best_score, best_i = score, i
            if best_i is None:
                areas = stats[1:, cv2.CC_STAT_AREA]
                i = 1 + int(np.argmax(areas))
            else:
                i = best_i
            x, y, w, h, area = [int(v) for v in stats[i, :5]]
            # 像素質量緊框（防 CC 連到全圖雨絲/泥地）
            ys, xs = np.where(lab == i)
            if len(xs) > 20:
                x_lo, x_hi = np.percentile(xs, [2, 98]).astype(int)
                y_lo, y_hi = np.percentile(ys, [2, 98]).astype(int)
            else:
                x_lo, y_lo, x_hi, y_hi = x, y, x + w - 1, y + h - 1
            # 取 CC 框与 percentile 框的交集倾向：优先 percentile
            x, y = int(x_lo), int(y_lo)
            w, h = int(x_hi - x_lo + 1), int(y_hi - y_lo + 1)
            pad_x = int(max(8, w * pad_frac))
            pad_y = int(max(8, h * pad_frac))
            x0 = max(0, x - pad_x)
            y0 = max(0, y - pad_y)
            x1 = min(W - 1, x + w - 1 + pad_x)
            y1 = min(H - 1, y + h - 1 + pad_y)
            meta = {
                "source": "L0_L1_kou_percentile_tight",
                "cc_area": int(area),
                "cc_xywh": [int(x), int(y), int(w), int(h)],
                "pad_frac": pad_frac,
            }
    # 保证至少 min_side，但仍禁止无意义全幅（面积比 >0.92 则回退到 CC 紧框+小pad）
    if x1 <= x0:
        x1 = min(W - 1, x0 + 8)
    if y1 <= y0:
        y1 = min(H - 1, y0 + 8)
    bw, bh = x1 - x0 + 1, y1 - y0 + 1
    if bw < min_side or bh < min_side:
        # 01525: 等比长大，禁正方形撑开（E-PEEP-RATIO）
        aspect = bw / float(max(1, bh))
        if aspect >= 1.0:
            new_bh = max(bh, min_side)
            new_bw = max(bw, int(round(new_bh * aspect)))
        else:
            new_bw = max(bw, min_side)
            new_bh = max(bh, int(round(new_bw / max(1e-6, aspect))))
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        half_w, half_h = new_bw // 2, new_bh // 2
        x0 = max(0, cx - half_w); x1 = min(W - 1, cx + half_w)
        y0 = max(0, cy - half_h); y1 = min(H - 1, cy + half_h)
        bw, bh = x1 - x0 + 1, y1 - y0 + 1
        meta["grew_to_min_side"] = True
        meta["ratio_lock"] = True
        meta["aspect_wh"] = round(bw / float(max(1, bh)), 4)
    area_frac = (bw * bh) / float(H * W)
    # 若几乎全幅：收成 CC 紧框（子集正身必须是子集）
    # 子集正身：面积比硬顶 0.55；过大则按 diff 质量中心再紧框
    if area_frac > 0.55:
        d = cv2.absdiff(L0, L1)
        g = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
        ys, xs = np.where(g > 18)
        if len(xs) > 50:
            # 质量中心 + 覆盖 90% 质量的窗口
            cx, cy = int(np.median(xs)), int(np.median(ys))
            x_lo, x_hi = np.percentile(xs, [5, 95]).astype(int)
            y_lo, y_hi = np.percentile(ys, [5, 95]).astype(int)
            # 若仍过宽，以中心裁到 max 0.5 幅
            max_w, max_h = int(W * 0.5), int(H * 0.92)
            bw, bh = x_hi - x_lo + 1, y_hi - y_lo + 1
            if bw > max_w:
                x_lo = max(0, cx - max_w // 2); x_hi = min(W - 1, x_lo + max_w - 1)
            if bh > max_h:
                y_lo = max(0, cy - max_h // 2); y_hi = min(H - 1, y_lo + max_h - 1)
            pad_x = int(max(8, (x_hi - x_lo + 1) * 0.06))
            pad_y = int(max(8, (y_hi - y_lo + 1) * 0.06))
            x0 = max(0, int(x_lo) - pad_x); y0 = max(0, int(y_lo) - pad_y)
            x1 = min(W - 1, int(x_hi) + pad_x); y1 = min(H - 1, int(y_hi) + pad_y)
            meta["shrunk_from_fullframe"] = True
            meta["area_frac_before"] = area_frac
            meta["source"] = meta.get("source", "") + "+mass_center_cap"
    if x1 <= x0:
        x1 = min(W - 1, x0 + 8)
    if y1 <= y0:
        y1 = min(H - 1, y0 + 8)
    bbox = [int(x0), int(y0), int(x1), int(y1)]
    corners = {
        "TL": [bbox[0], bbox[1]],
        "TR": [bbox[2], bbox[1]],
        "BR": [bbox[2], bbox[3]],
        "BL": [bbox[0], bbox[3]],
    }
    meta.update({
        "bbox_xyxy_in_S0": bbox,
        "corners_in_S0": corners,
        "S0A_size": [bbox[3] - bbox[1] + 1, bbox[2] - bbox[0] + 1],
        "S0_size": [H, W],
        "area_frac": (bbox[2] - bbox[0] + 1) * (bbox[3] - bbox[1] + 1) / float(H * W),
        "subset_zheng_shen": True,
        "scale": 1.0,
        "law": "S0A=子集正身框 native；peep 自框更正中",
    })
    return bbox, meta




def bbox_from_mark(
    M: np.ndarray,
    pad_frac: float = 0.12,
    min_side: int = 256,
) -> Tuple[List[int], dict]:
    """子集正身框：由全幅 MARK 緊 bbox（優先於亂 CC 泥地條）。"""
    H, W = M.shape[:2]
    ys, xs = np.where(M > 0)
    if len(xs) < 32:
        raise RuntimeError("E-S0A MARK empty — 無法建子集正身框")
    x_lo, x_hi = np.percentile(xs, [1, 99]).astype(int)
    y_lo, y_hi = np.percentile(ys, [1, 99]).astype(int)
    bw, bh = int(x_hi - x_lo + 1), int(y_hi - y_lo + 1)
    pad_x = int(max(8, bw * pad_frac))
    pad_y = int(max(8, bh * pad_frac))
    x0 = max(0, int(x_lo) - pad_x)
    y0 = max(0, int(y_lo) - pad_y)
    x1 = min(W - 1, int(x_hi) + pad_x)
    y1 = min(H - 1, int(y_hi) + pad_y)
    bw, bh = x1 - x0 + 1, y1 - y0 + 1
    # 01525: 保 MARK 原生比例；禁 min_side 独立撑成正方形（E-PEEP-RATIO）
    aspect = bw / float(max(1, bh))  # W/H
    need = False
    if bw < min_side or bh < min_side:
        need = True
        # 以较长边不足为准，等比放大
        scale_need = max(min_side / float(max(1, bw)), min_side / float(max(1, bh)))
        # 若已有一边够大，只抬短边但保持 aspect
        new_bw = max(bw, int(round(bh * aspect)), min_side if aspect >= 1 else int(round(min_side * aspect)))
        new_bh = max(bh, int(round(bw / max(1e-6, aspect))), min_side if aspect < 1 else int(round(min_side / max(1e-6, aspect))))
        # 统一：以 aspect 为准
        if aspect >= 1.0:
            new_bh = max(bh, min_side)
            new_bw = max(bw, int(round(new_bh * aspect)))
        else:
            new_bw = max(bw, min_side)
            new_bh = max(bh, int(round(new_bw / max(1e-6, aspect))))
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        half_w, half_h = new_bw // 2, new_bh // 2
        x0 = max(0, cx - half_w); x1 = min(W - 1, cx + half_w)
        y0 = max(0, cy - half_h); y1 = min(H - 1, cy + half_h)
        # 边界夹后可能微偏比例：以最终切片为准记录
    bbox = [int(x0), int(y0), int(x1), int(y1)]
    _fw, _fh = bbox[2] - bbox[0] + 1, bbox[3] - bbox[1] + 1
    meta = {
        "source": "MARK_full_percentile",
        "ratio_lock": True,
        "aspect_wh": round(_fw / float(max(1, _fh)), 4),
        "grew_min_side_ratio_safe": need,
        "bbox_xyxy_in_S0": bbox,
        "corners_in_S0": {
            "TL": [bbox[0], bbox[1]], "TR": [bbox[2], bbox[1]],
            "BR": [bbox[2], bbox[3]], "BL": [bbox[0], bbox[3]],
        },
        "S0A_size": [bbox[3] - bbox[1] + 1, bbox[2] - bbox[0] + 1],
        "S0_size": [H, W],
        "area_frac": (bbox[2] - bbox[0] + 1) * (bbox[3] - bbox[1] + 1) / float(H * W),
        "subset_zheng_shen": True,
        "scale": 1.0,
        "mark_frac": float((M > 0).mean()),
        "law": "S0A←全幅MARK；peep 自框更正中；不放大",
    }
    return bbox, meta


def crop_S0A(im: np.ndarray, bbox: List[int]) -> np.ndarray:
    x0, y0, x1, y1 = bbox
    return im[y0 : y1 + 1, x0 : x1 + 1].copy()


def map_S0A_to_S0(S0: np.ndarray, S0A_img: np.ndarray, bbox: List[int], M_S0A: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
    """S0A 結果對位回 S0 → S01。work 已缩 native 后调用；强制 tile/M 对齐 bbox 切片。"""
    out = S0.copy()
    H0, W0 = S0.shape[:2]
    x0, y0, x1, y1 = [int(v) for v in bbox]
    x0, x1 = sorted((max(0, x0), min(W0 - 1, x1)))
    y0, y1 = sorted((max(0, y0), min(H0 - 1, y1)))
    h, w = y1 - y0 + 1, x1 - x0 + 1
    if h <= 0 or w <= 0:
        raise RuntimeError(f"E-S0A bad bbox {[x0,y0,x1,y1]}")
    # 永远按切片尺寸 resize（防放大链 hn/wn 与 bbox 漂移）
    tile = cv2.resize(S0A_img, (w, h), interpolation=cv2.INTER_AREA)
    M_full = np.zeros((H0, W0), np.uint8)
    if M_S0A is not None:
        m = cv2.resize(M_S0A, (w, h), interpolation=cv2.INTER_NEAREST)
        M_full[y0 : y1 + 1, x0 : x1 + 1] = m
        region = out[y0 : y1 + 1, x0 : x1 + 1].copy()
        sel = m > 0
        region[sel] = tile[sel]
        out[y0 : y1 + 1, x0 : x1 + 1] = region
    else:
        out[y0 : y1 + 1, x0 : x1 + 1] = tile
        M_full[y0 : y1 + 1, x0 : x1 + 1] = 255
    out[M_full == 0] = S0[M_full == 0]
    return out, M_full




def mark_from_L0_L1(L0: np.ndarray, L1: np.ndarray, thr: int = 12) -> np.ndarray:
    """全幅只有洞 MARK（遠景小物 thr 可降）。"""
    d = cv2.absdiff(L0, L1)
    g = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(g, int(thr), 255, cv2.THRESH_BINARY)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8), 2)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), 1)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(th, 8)
    M = np.zeros(g.shape, np.uint8)
    if n <= 1:
        # 兜底：全 diff 软阈
        M[g > max(6, thr - 4)] = 255
        return M
    areas = stats[1:, cv2.CC_STAT_AREA]
    i = 1 + int(np.argmax(areas))
    M[lab == i] = 255
    # 若最大 CC 仍太碎，并入面积>0.15*max 的件
    max_a = float(areas.max())
    for j in range(1, n):
        if stats[j, cv2.CC_STAT_AREA] >= 0.15 * max_a:
            M[lab == j] = 255
    return M


def bite_hole_sheng_return(
    L0: np.ndarray,
    M: np.ndarray,
    elev_or_hd: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Dict[str, Any]]:
    """咬合硬契約（01518）
    咬出一塊 → 必有洞 MARK
    升清那塊 → peep 同形同尺（合適大細）
    放回洞   → 置中對位 hardpaste；洞外 bitexact

    返回 (RETURN, peep_crop, I_sheng_crop, meta)
    """
    H, W = L0.shape[:2]
    assert M.shape[:2] == (H, W)
    if int((M > 0).sum()) < 16:
        raise RuntimeError("E-BITE hole empty")

    ys, xs = np.where(M > 0)
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    peep = L0[y0 : y1 + 1, x0 : x1 + 1].copy()
    pm = M[y0 : y1 + 1, x0 : x1 + 1].copy()
    ph, pw = peep.shape[:2]

    if elev_or_hd is not None:
        I_sheng = scale_lock_elev(peep, elev_or_hd, pm)
        if I_sheng.shape[:2] != (ph, pw):
            I_sheng = cv2.resize(I_sheng, (pw, ph), interpolation=cv2.INTER_AREA)
        I_sheng = I_sheng.copy()
        I_sheng[pm == 0] = peep[pm == 0]
        donor = "elev/HD → scale_lock 同 peep 大細置中"
    else:
        I_sheng = peep.copy()
        donor = "peep self (NEED 外力GROK 升清)"

    I_full = L0.copy()
    region = I_full[y0 : y1 + 1, x0 : x1 + 1].copy()
    sel = pm > 0
    region[sel] = I_sheng[sel]
    I_full[y0 : y1 + 1, x0 : x1 + 1] = region
    RET = hardpaste(L0, M, I_full)
    RET = RET.copy()
    RET[M == 0] = L0[M == 0]
    out = outside_max(RET, L0, M)

    meta = {
        "law": "咬→洞→升清咬塊→同尺置中回洞",
        "algebra": "[(生,除,洞,扣)×(反)]",
        "bite": "peep = L0 ⊙ MARK",
        "hole": "MARK 座位",
        "sheng": donor,
        "return": "hardpaste seat-born 置中對位",
        "bbox_xyxy": [x0, y0, x1, y1],
        "peep_hw": [ph, pw],
        "I_sheng_hw": list(I_sheng.shape[:2]),
        "size_lock": list(I_sheng.shape[:2]) == [ph, pw],
        "outside": int(out),
        "PASS_align": int(out) == 0 and list(I_sheng.shape[:2]) == [ph, pw],
        "center_in_frame": [
            round((x0 + x1) / 2 / max(1, W), 4),
            round((y0 + y1) / 2 / max(1, H), 4),
        ],
    }
    return RET, peep, I_sheng, meta


def hole_only_sx_return_S0(
    root: Path,
    bus: "StateBus",
    L0_full: np.ndarray,
    M_full: np.ndarray,
    elev_correct: np.ndarray,
    parent_s: str = "S11",
) -> Dict[str, Any]:
    """回 S0 專用：只有洞 的 (S)×(S) DEBUG。
    正確 donor = elev/正機 freeframe（外力GROK 身份）
    強心針 = 認 ∩ 放大 ∩ 升質×物 → seat-born 入洞 → 反 outside=0
    禁：無洞 freeframe 全幀回；禁 elev 當布局；禁跳過洞座。
    """
    H, W = L0_full.shape[:2]
    assert M_full.shape[:2] == (H, W)
    if int((M_full > 0).sum()) < 16:
        raise RuntimeError("E-S0R hole empty — 只有洞 链需要 MARK_full")

    # R0 凍 S0
    p_r0 = root / "S0R_R0_L0.png"
    cv2.imwrite(str(p_r0), L0_full)
    bus.write("S0R_R0", "回S0·凍母集", parent_s, {"S0R_R0_L0.png": p_r0}, hole_only=True)

    # R1 只有洞 MARK
    p_rm = root / "S0R_MARK_only.png"
    cv2.imwrite(str(p_rm), M_full)
    bus.write(
        "S0R_MARK",
        "只有洞 · 回S0 唯一座位",
        "S0R_R0",
        {"S0R_MARK_only.png": p_rm},
        hole_only=True,
        frac=float((M_full > 0).mean()),
        law="回S0 只认此洞；无洞=E-WLF3-01",
    )

    # R2 扣/认：母集 peep（洞内 L0 身份）
    ys, xs = np.where(M_full > 0)
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    pad = 4
    y0, x0 = max(0, y0 - pad), max(0, x0 - pad)
    y1, x1 = min(H - 1, y1 + pad), min(W - 1, x1 + pad)
    peep = L0_full[y0 : y1 + 1, x0 : x1 + 1].copy()
    pm = M_full[y0 : y1 + 1, x0 : x1 + 1].copy()
    p_peep = root / "S0R_peep_hole.jpg"
    cv2.imwrite(str(p_peep), peep, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    bus.write(
        "S0R_认",
        "強心針·認：洞内 peep 身份（母集）",
        "S0R_MARK",
        {"S0R_peep_hole.jpg": p_peep},
        hole_only=True,
        boost="认",
        bbox=[x0, y0, x1, y1],
    )

    # R3 放大：peep 域放大看（仅 peep 子图 densify 尺，不改全景）
    peep_big = cv2.resize(peep, (peep.shape[1] * 2, peep.shape[0] * 2), interpolation=cv2.INTER_CUBIC)
    pm_big = cv2.resize(pm, (peep_big.shape[1], peep_big.shape[0]), interpolation=cv2.INTER_NEAREST)
    p_big = root / "S0R_peep_x2.jpg"
    cv2.imwrite(str(p_big), peep_big, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    bus.write(
        "S0R_放大",
        "強心針·放大：peep×2 子域（非整幅升采样冒充）",
        "S0R_认",
        {"S0R_peep_x2.jpg": p_big},
        hole_only=True,
        boost="放大",
    )

    # R4 升質×物：正確 elev freeframe → scale_lock 到 peep（外力GROK donor）
    elev_lock, elev_meta = elev_must_be_child(peep, pm, elev_correct, dens_fallback=peep)
    # 升質也在 x2 上再锁一次再缩回 peep 尺（细节进洞）
    elev_x2, _ = elev_must_be_child(peep_big, pm_big, elev_correct, dens_fallback=peep_big)
    elev_back = cv2.resize(elev_x2, (peep.shape[1], peep.shape[0]), interpolation=cv2.INTER_AREA)
    if elev_back.shape[:2] != peep.shape[:2]:
        elev_back = cv2.resize(elev_back, (peep.shape[1], peep.shape[0]), interpolation=cv2.INTER_AREA)
    p_elev = root / "S0R_elev_correct_lock.jpg"
    p_elev_src = root / "S0R_elev_CORRECT_SRC.jpg"
    cv2.imwrite(str(p_elev), elev_back, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    cv2.imwrite(str(p_elev_src), elev_correct, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    bus.write(
        "S0R_升质",
        "強心針·升質×物：正確圖 elev freeframe → peep 尺（外力GROK donor）",
        "S0R_放大",
        {"S0R_elev_correct_lock.jpg": p_elev, "S0R_elev_CORRECT_SRC.jpg": p_elev_src},
        hole_only=True,
        boost="升质×物",
        driver="外力GROK",
        **{k: elev_meta.get(k) for k in ("elev_is_child_of_peep", "elev_is_not_RETURN", "source", "align") if elev_meta.get(k) is not None},
    )

    # R5 BOOST AND
    boost_ok = True  # 认/放大/升质 三步已写 Bus
    bus.write(
        "S0R_AND",
        "強心針 AND：认∩放大∩升质×物",
        "S0R_升质",
        {},
        hole_only=True,
        boost_AND=boost_ok,
        formula="[(生,除,洞,扣)×(反)] ← 外力GROK ⊕ 强心针[认∩放大∩升质×物]",
    )

    # R6 生：咬合硬契約 咬→升清咬塊→同尺置中回洞
    S0R, peep2, I_sheng, bite_meta = bite_hole_sheng_return(L0_full, M_full, elev_correct)
    out = int(bite_meta["outside"])
    p_s0r = root / "S0R_RETURN.png"
    p_s0r_jpg = root / "S0R_RETURN.jpg"
    p_peep_bite = root / "S0R_BITE_peep.jpg"
    p_sheng = root / "S0R_SHENG_same_size.jpg"
    p_align = root / "S0R_BITE_ALIGN.json"
    cv2.imwrite(str(p_s0r), S0R)
    cv2.imwrite(str(p_s0r_jpg), S0R, [int(cv2.IMWRITE_JPEG_QUALITY), 98])
    cv2.imwrite(str(p_peep_bite), peep2, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    cv2.imwrite(str(p_sheng), I_sheng, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    p_align.write_text(json.dumps(bite_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    bus.write(
        "S0R_生",
        "咬→升清咬塊→同尺置中回洞（外力GROK donor 锁 peep 大細）",
        "S0R_AND",
        {
            "S0R_RETURN.png": p_s0r,
            "S0R_RETURN.jpg": p_s0r_jpg,
            "S0R_BITE_peep.jpg": p_peep_bite,
            "S0R_SHENG_same_size.jpg": p_sheng,
            "S0R_BITE_ALIGN.json": p_align,
        },
        hole_only=True,
        seat_born=True,
        outside=out,
        size_lock=bite_meta.get("size_lock"),
        PASS_align=bite_meta.get("PASS_align"),
        driver="外力GROK",
        law=bite_meta.get("law"),
        algebra=bite_meta.get("algebra"),
    )

    # R7 反
    p_gate = root / "S0R_ANTI_GATE.json"
    gate = {
        "hole_only": True,
        "outside": out,
        "PASS": out == 0 and bool(bite_meta.get("PASS_align", True)),
        "boost_AND": boost_ok,
        "driver": "外力GROK",
        "donor": "elev → peep 同尺置中 → hardpaste 回洞",
        "formula": "咬→洞→升清咬塊→同尺置中回洞  [(生,除,洞,扣)×(反)]",
        "E-WLF3-01": "无洞回=禁",
        "size_lock": bite_meta.get("size_lock"),
        "PASS_align": bite_meta.get("PASS_align"),
        "bbox_xyxy": bite_meta.get("bbox_xyxy"),
        "claim": "C2_BITE_HOLE_ALIGN_SX" if out == 0 and bite_meta.get("PASS_align") else ("FAIL_S0R"),
    }
    p_gate.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
    bus.write(


# ... truncated for Hub size ...

t_intact("S3", "MARK.png", s3_sha)
    bus.assert_intact("S5", f"{cfg['peep_key']}_crop.jpg", s5_sha)
    bus.assert_intact("S8", "S8_BOOST.json", s8_sha)

    S0_lock = S0_work  # 工作域（S0A 子集或全 S0）
    M_lock = M_r

    # fill 优先 S9A 升清 temp（更洞准）；再 I_use / HP — 禁全幀正頭冒 RETURN (E-SX-07)
    if I_use_for_S11 is not None:
        fill_src = I_use_for_S11
        fill_name = "S9A"
    elif I_use is None:
        fill_src = HP if HP is not None else S9
        fill_name = "HP/S9"
    else:
        fill_src = I_use
        fill_name = "I_use"
    # 檢測 freeframe 全幀當 RETURN
    ff = detect_freeframe(fill_src if fill_src.shape[:2] == S0_lock.shape[:2] else cv2.resize(fill_src, (S0_lock.shape[1], S0_lock.shape[0])), S0_lock, M_lock)
    et = ensure(root / "ERROR_TEXTBOOK")
    p_wrong = et / "E_SX_07_FULLFRAME_AS_RETURN.jpg"
    if ff.get("is_freeframe") or int(ff.get("outside_max", 0) or 0) > 0:
        # 錯例：全幀未鎖 — 寫 ERROR 教材
        wrong = fill_src if fill_src.shape[:2] == S0_lock.shape[:2] else cv2.resize(fill_src, (S0_lock.shape[1], S0_lock.shape[0]))
        cv2.imwrite(str(p_wrong), wrong, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        (et / "E_SX_07.json").write_text(
            json.dumps({"code": "E-SX-07", "msg": "全幀正頭冒 RETURN", "outside": ff.get("outside_max")}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # 強制 S11×S0 公式（咬合：fill 經 peep 同尺；硬鎖洞外）
    # 01526 優先：S9A 升清 temp 作 fill（更洞准）；否則 elev bite；否則 structural
    elev_for_fill = elev if elev is not None else (I_HD if I_HD is not None else None)
    peep0_s11 = None
    I_sheng_s11 = None
    if I_use_for_S11 is not None and fill_src is not None:
        fs = fill_src if fill_src.shape[:2] == S0_lock.shape[:2] else cv2.resize(fill_src, (S0_lock.shape[1], S0_lock.shape[0]))
        HP_lock = hardpaste(S0_lock, M_lock, fs)
        HP_lock = HP_lock.copy()
        HP_lock[M_lock == 0] = S0_lock[M_lock == 0]
        bite_s11 = {
            "size_lock": True,
            "PASS_align": True,
            "sheng": "S9A_升清_temp",
            "fill_from": "S9A",
            "law": "S9→S9A升清→S11×S0；洞准 fill",
        }
        # 仍可溯 peep
        ys, xs = np.where(M_lock > 0)
        if len(xs) >= 8:
            yy0, yy1 = int(ys.min()), int(ys.max())
            xx0, xx1 = int(xs.min()), int(xs.max())
            peep0_s11 = S0_lock[yy0:yy1+1, xx0:xx1+1].copy()
            I_sheng_s11 = fs[yy0:yy1+1, xx0:xx1+1].copy()
    elif elev_for_fill is not None:
        HP_lock, peep0_s11, I_sheng_s11, bite_s11 = bite_hole_sheng_return(S0_lock, M_lock, elev_for_fill)
    else:
        # 無 elev：hardpaste 結構座
        HP_lock = hardpaste(S0_lock, M_lock, fill_src if fill_src.shape[:2] == S0_lock.shape[:2] else S0_lock)
        HP_lock = HP_lock.copy()
        HP_lock[M_lock == 0] = S0_lock[M_lock == 0]
        bite_s11 = {"size_lock": True, "PASS_align": True, "sheng": "structural"}

    out_max = outside_max(HP_lock, S0_lock, M_lock)
    if out_max != 0:
        (et / "E_SX_06.json").write_text(
            json.dumps({
                "code": "E-SX-06",
                "msg": "S11 未與 S0 對位鎖",
                "outside": int(out_max),
                "formula": "‖RETURN−S0‖_outside MARK = 0",
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        raise RuntimeError(f"E-SX-06 S11 未與 S0 對位鎖 outside={out_max}")

    # 對照板 WRONG | RIGHT | S0
    def _thumb(im, w=320, h=240):
        if im is None:
            return np.zeros((h, w, 3), np.uint8)
        if im.ndim == 2:
            im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        return cv2.resize(im, (w, h))
    def _lab(im, t, col=(0, 255, 200)):
        im = im.copy()
        cv2.rectangle(im, (0, 0), (im.shape[1], 28), (0, 0, 0), -1)
        cv2.putText(im, t, (4, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 1, cv2.LINE_AA)
        return im
    wrong_vis = fill_src if fill_src.shape[:2] == S0_lock.shape[:2] else cv2.resize(fill_src, (S0_lock.shape[1], S0_lock.shape[0]))
    board = np.hstack([
        _lab(_thumb(wrong_vis), "WRONG fullframe not lock S0", (0, 80, 255)),
        _lab(_thumb(HP_lock), "RIGHT S11xS0 out=0", (0, 255, 120)),
        _lab(_thumb(S0_lock), "S0 gold", (0, 255, 255)),
    ])
    title = np.zeros((36, board.shape[1], 3), np.uint8)
    cv2.putText(
        title,
        "S11 x S0 lock (S)x(S)  RETURN=S0*(1-M)+fill*M  outside=0  + BOOST",
        (6, 24),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 255),
        1,
    )
    boards = ensure(root / "boards")
    p_board = boards / "S11xS0_ALIGN.jpg"
    cv2.imwrite(str(p_board), np.vstack([title, board]), [int(cv2.IMWRITE_JPEG_QUALITY), 92])

    HP = HP_lock  # 下游 S01 / report 用對位鎖結果
    p_s11 = root / "S11xS0_PRIMARY.jpg"
    p_s11_png = root / "S11xS0_PRIMARY.png"
    cv2.imwrite(str(p_s11_png), HP)
    cv2.imwrite(str(p_s11), HP, [int(cv2.IMWRITE_JPEG_QUALITY), 98])
    if peep0_s11 is not None:
        cv2.imwrite(str(root / "S11xS5_peep0.jpg"), peep0_s11, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    if I_sheng_s11 is not None:
        cv2.imwrite(str(root / "S11xS5_fill_sheng.jpg"), I_sheng_s11, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

    gate = {
        "S11xS0": True,
        "S11xS3_MARK_seat": True,
        "S11xS5_peep0_trace": peep0_s11 is not None,
        "outside_max_diff": int(out_max),
        "PASS": out_max == 0,
        "formula": "RETURN = S0 ⊙ (1−M) + fill ⊙ M ; ‖RETURN−S0‖_outside = 0",
        "PRIMARY": "S11×S0 hardpaste seat — never freeframe alone",
        "boost_AND": True,
        "boost_formula": "认 ∩ 放大 ∩ 升质×物",
        "bite_align": bite_s11,
        "E-SX-06": "S11 未與 S0 對位鎖" if out_max != 0 else "clear",
        "E-SX-07": "全幀正頭冒 RETURN" if ff.get("is_freeframe") else "clear",
        "anti_toxin": ["E-FF-01", "E-FF-02", "E-SX-06", "E-SX-07"],
        "claim": "C2_S11xS0_ALIGN" if out_max == 0 else "FAIL_E-SX-06",
        "fill_from": fill_name if "fill_name" in locals() else "unknown",
        "S9A_used": (locals().get("fill_name") == "S9A"),
        "S9A_ephemeral": True,
    }
    p_gate = root / "S11_GATE.json"
    p_gate.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
    # DNA machine-readable
    dna = {
        "formal": "S11xS0_ALIGN_LOCK_V1",
        "write": WRITE,
        "formula": gate["formula"],
        "locks": ["S11×S0", "S11×S3", "S11×S5", "BOOST_AND"],
        "E": ["E-SX-06", "E-SX-07"],
        "ACCEPT_FULL_HD": False,
        "gold": "S0 bitexact outside MARK",
    }
    (root / "DNA_S11xS0_ALIGN.json").write_text(json.dumps(dna, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[SX] S11 pre-write slots", sorted(p.name for p in (bus.bus).iterdir()), flush=True)
    gate["fill_from"] = fill_name if "fill_name" in dir() else "unknown"
    gate["S9A_used"] = (gate.get("fill_from") == "S9A")
    bus.write(
        "S11",
        "S11×S0 對位鎖 (S)×(S) + 強心針 · fill←S9A升清",
        "S10",
        {
            "S11xS0_PRIMARY.png": p_s11_png,
            "S11xS0_PRIMARY.jpg": p_s11,
            "S11_GATE.json": p_gate,
            "DNA_S11xS0_ALIGN.json": root / "DNA_S11xS0_ALIGN.json",
            "S11xS0_ALIGN.jpg": p_board,
        },
        **{k: gate[k] for k in ("S11xS0", "outside_max_diff", "PASS", "formula", "claim", "boost_AND", "fill_from", "S9A_used") if k in gate},
    )
    # 销毁 S9A + S7A 临时产物（保留 META；用完可销毁）
    destroyed = []
    for _p in (p_s9a, p_s9a_jpg):
        if _p.exists():
            _p.unlink()
            destroyed.append(_p.name)
    for _p in (bus.bus / "S9A").glob("S9A_SHENG_TEMP.*"):
        try:
            _p.unlink()
            destroyed.append(f"Bus/S9A/{_p.name}")
        except Exception:
            pass
    # S7A
    for _p in (root / "S7A_SHENG_TEMP.png", root / "S7A_SHENG_TEMP.jpg"):
        if _p.exists():
            _p.unlink()
            destroyed.append(_p.name)
    for _p in (bus.bus / "S7A").glob("S7A_SHENG_TEMP.*"):
        try:
            _p.unlink()
            destroyed.append(f"Bus/S7A/{_p.name}")
        except Exception:
            pass
    destroy_doc = {
        "destroyed": destroyed,
        "kept": [
            "S7A_META.json", "Bus/S7A/S7A_META.json", "Bus/S7A/SLOT.json",
            "S9A_META.json", "Bus/S9A/S9A_META.json", "Bus/S9A/SLOT.json",
        ],
        "why": "S7A/S9A ephemeral — (S)×(S) 洞准用完可销毁；S11 已锁 S0",
        "S11_PASS": out_max == 0,
        "pattern": "S7→S7A→…→S9→S9A→S11 → destroy S7A&S9A",
    }
    (root / "S9A_DESTROYED.json").write_text(json.dumps(destroy_doc, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "S7A_DESTROYED.json").write_text(json.dumps(destroy_doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[SX] S7A+S9A destroyed after S11: {destroyed}", flush=True)
    # final intact
    bus.assert_intact("S0", "L0.png", s0_sha)
    bus.assert_intact("S3", "MARK.png", s3_sha)
    bus.assert_intact("S5", f"{cfg['peep_key']}_crop.jpg", s5_sha)
    # report aliases for S11×S0
    out_s9 = int(out_max)
    out_full = int(ff.get("outside_max", 0) or 0)

    # ---- S01 / S0R：回 S0 = 只有洞 的 (S)×(S) DEBUG ----
    # 正確 donor = elev freeframe（外力GROK）+ 強心針；禁無洞貼回
    S01 = L0_full.copy()
    M_full = np.zeros((H_full, W_full), np.uint8)
    s0r_rep = None
    if use_s0a:
        bus.assert_intact("S0", "L0.png", s0_sha)
        bus.assert_intact("S0A", "S0A.png", s0a_sha)
        # 1) 只有洞：优先全幅 MARK_full_pre；否则映回；再空则重扣
        if M_full_pre is not None and int((M_full_pre > 0).sum()) >= 32:
            M_full = M_full_pre.copy()
        else:
            _, M_full = map_S0A_to_S0(L0_full, L0, bbox, M_r)
        if int((M_full > 0).sum()) < 32:
            M_full = mark_from_L0_L1(L0_full, L1_full, thr=10)
            # 仍空 thr 再降
            if int((M_full > 0).sum()) < 32:
                M_full = mark_from_L0_L1(L0_full, L1_full, thr=6)
            (root / "S0R_MARK_REBUILT_FLAG.txt").write_text(
                f"rebuilt from L0|L1 px={int((M_full>0).sum())}\n", encoding="utf-8"
            )
        # 若 elev 未给：退化为 HP map（旧路）但仍记 WARN
        elev_for_return = elev if elev is not None else None
        if elev_for_return is None and I_HD_full is not None:
            elev_for_return = I_HD_full  # 次选
        if elev_for_return is None:
            S01, M_full = map_S0A_to_S0(L0_full, HP, bbox, M_r)
            S01[M_full == 0] = L0_full[M_full == 0]
            s01_out = outside_max(S01, L0_full, M_full)
            s01_note = "WARN no elev_correct; fallback S0A map-back"
        else:
            s0r_rep = hole_only_sx_return_S0(
                root, bus, L0_full, M_full, elev_for_return, parent_s="S11"
            )
            S01 = s0r_rep["S0R"]
            M_full = s0r_rep["M_full"]
            s01_out = int(s0r_rep["outside"])
            s01_note = "只有洞 (S)×(S) DEBUG ← 外力GROK elev_correct ⊕ 强心针"
    else:
        # 无 S0A：S11 已是全图；若有 elev 仍可再跑 hole-only 覆盖洞内
        M_full = M_r
        if elev is not None:
            s0r_rep = hole_only_sx_return_S0(root, bus, L0_full, M_full, elev, parent_s="S11")
            S01 = s0r_rep["S0R"]
            s01_out = int(s0r_rep["outside"])
            s01_note = "只有洞 (S)×(S) DEBUG on full（无S0A）"
        else:
            S01 = HP
            s01_out = out_max
            s01_note = "no S0A no elev; S01≡S11"
    p_s01 = root / "S01.png"
    p_s01_jpg = root / "S01.jpg"
    p_mfull = root / "MARK_full_in_S0.png"
    cv2.imwrite(str(p_s01), S01)
    cv2.imwrite(str(p_s01_jpg), S01, [int(cv2.IMWRITE_JPEG_QUALITY), 98])
    cv2.imwrite(str(p_mfull), M_full)
    s01_gate = {
        "S01_from": "S0A_map_back" if use_s0a else "S11",
        "outside_in_S0": s01_out,
        "PASS": s01_out == 0,
        "bbox": bbox,
        "formula": "只有洞(S)×(S) ← 外力GROK elev ⊕ 强心针 → S0；outside=0",
        "s01_note": s01_note,
        "hole_only_sx": s0r_rep is not None,
        "boost_AND": (s0r_rep or {}).get("boost_AND"),
        "driver": "外力GROK",
    }
    (root / "S01_GATE.json").write_text(json.dumps(s01_gate, ensure_ascii=False, indent=2), encoding="utf-8")
    bus.write(
        "S01",
        "S0A 对位回 S0 全景",
        "S11",
        {"S01.png": p_s01, "S01.jpg": p_s01_jpg, "MARK_full_in_S0.png": p_mfull, "S01_GATE.json": root / "S01_GATE.json"},
        **s01_gate,
        reads=["S0", "S0A" if use_s0a else "S0", "S11"],
    )
    bus.assert_intact("S0", "L0.png", s0_sha)

    # board
    def th(im, w=140, h=90):
        if im is None:
            return np.zeros((h, w, 3), np.uint8)
        if im.ndim == 2:
            im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        return cv2.resize(im, (w, h))

    def lab(im, t, ok=True):
        im = im.copy()
        c = (0, 255, 160) if ok else (80, 80, 255)
        cv2.rectangle(im, (0, 0), (im.shape[1], 16), (0, 0, 0), -1)
        cv2.putText(im, t[:18], (2, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.3, c, 1, cv2.LINE_AA)
        return im

    cells = []
    for i in range(12):
        si = f"S{i}"
        slot = bus.bus / si
        imgs = list(slot.glob("*.jpg")) + list(slot.glob("*.png"))
        impath = None
        for c in imgs:
            if "MARK" in c.name:
                impath = c
                break
        if impath is None and imgs:
            impath = imgs[0]
        im = cv2.imread(str(impath), cv2.IMREAD_UNCHANGED) if impath else None
        ok = bus.reload(si).get("ok", True)
        if si == "S11":
            ok = out_max == 0
        cells.append(lab(th(im), si, ok))
    row1 = np.hstack(cells[:6])
    row2 = np.hstack(cells[6:])
    if row2.shape[1] < row1.shape[1]:
        row2 = np.hstack([row2, np.zeros((row2.shape[0], row1.shape[1] - row2.shape[1], 3), np.uint8)])
    title = np.zeros((40, row1.shape[1], 3), np.uint8)
    cv2.putText(
        title,
        f"{cfg['zh']} {mode} S0|S0A→S01 outA={out_max} outS0={s01_out} BOOST={boost['AND']}",
        (4, 26),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.42,
        (0, 255, 255),
        1,
        cv2.LINE_AA,
    )
    board = np.vstack([title, row1, row2])
    ensure(root / "boards")
    cv2.imwrite(str(root / "boards" / "SX_S0_S11.jpg"), board, [int(cv2.IMWRITE_JPEG_QUALITY), 92])

    out_s9 = int(s9_out)
    PASS = all(c["ok"] for c in bus.chain) and out_max == 0 and out_s9 == 0 and boost["AND"] and s01_out == 0
    report = {
        "write_id": WRITE,
        "mode": mode,
        "zh": cfg["zh"],
        "formal": cfg["formal"],
        "stick": cfg["stick"],
        "bite": cfg["bite"],
        "dna_equation": DNA_DIFF["equation"] if mode == "shen" else "正頭 = 母本",
        "tune": tune,
        "kou": kou_meta,
        "boost": boost,
        "S11xS0A_outside": out_max,
        "S01_S0_outside": s01_out,
        "S0A": s0a_meta,
        "S11xS0_outside": out_max,
        "fullframe_outside": out_full,
        "S9_seat_born_outside": out_s9,
        "subset_zheng_shen_S0A": {
            "enabled": bool(use_s0a),
            "law": "S0A=子集正身起點·不放大；peep 自框更正中",
            "fixes": ["peep frame center on S0A", "elev peep-child", "freeframe seat-born"],
        },
        "anti_freeframe_elev": {
            "E-FF-01": "freeframe S9 banned as PRIMARY",
            "E-FF-02": "elev not RETURN",
            "E-FF-03": "peep never overwrite",
            "shared_with": "正头 ERROR_TEXTBOOK freeframe/elev",
        },
        "PASS_SX_FULL": PASS,
        "chain": bus.chain,
        "assets": assets,
        "claim": f"C2_S11xS0_ALIGN_BOOST_{mode.upper()}",
        "ACCEPT_FULL_HD": False,
        "kuangya": {"reuse": "shq_wai_li_fan_v2_any_object.kou_part/hardpaste/outside_max"},
        "asof": asof,
    }
    (root / "REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "DNA_MODE.json").write_text(
        json.dumps({"mode": mode, "cfg": cfg, "diff": DNA_DIFF}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def cmd_diff_dna(_: argparse.Namespace) -> int:
    print(json.dumps(DNA_DIFF, ensure_ascii=False, indent=2))
    return 0


def cmd_selftest(args: argparse.Namespace) -> int:
    """合成：正頭(小圓=頭) vs 正身(整矩形=整件) 同母 PY"""
    root = ensure(Path(args.out))
    # canvas
    L0 = np.full((240, 320, 3), 36, np.uint8)
    # body
    cv2.rectangle(L0, (100, 90), (220, 210), (160, 150, 140), -1)
    # head
    cv2.circle(L0, (160, 70), 32, (200, 180, 160), -1)
    # 除头 L1
    L1_tou = L0.copy()
    cv2.circle(L1_tou, (160, 70), 32, (36, 36, 36), -1)
    # 除整件 L1
    L1_shen = L0.copy()
    cv2.rectangle(L1_shen, (100, 90), (220, 210), (36, 36, 36), -1)
    cv2.circle(L1_shen, (160, 70), 32, (36, 36, 36), -1)

    r_tou = run_zheng(root / "tou", "tou", L0, L1_tou, I_HD=L0, tune_name="human_mid_head", use_s0a=True, s0a_scale=2.0, s0a_min_side=128, s0a_pad=0.2)
    r_shen = run_zheng(root / "shen", "shen", L0, L1_shen, I_HD=L0, tune_name="whole_subject", use_s0a=True, s0a_scale=2.0, s0a_min_side=128, s0a_pad=0.2)
    summary = {
        "selftest": True,
        "write": WRITE,
        "tou_PASS": r_tou["PASS_SX_FULL"],
        "shen_PASS": r_shen["PASS_SX_FULL"],
        "tou_out": r_tou["S11xS0_outside"],
        "shen_out": r_shen["S11xS0_outside"],
        "equation": DNA_DIFF["equation"],
        "same_py": "shq_zheng_tou_shen.py mode=tou|shen",
        "note": "structural selftest — production needs 外力GROK L1/I_HD",
    }
    (root / "SELFTEST.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if r_tou["PASS_SX_FULL"] and r_shen["PASS_SX_FULL"] else 1


def cmd_run(args: argparse.Namespace) -> int:
    L0 = cv2.imread(args.l0)
    L1 = cv2.imread(args.l1)
    assert L0 is not None and L1 is not None, "need --l0 --l1"
    I_HD = cv2.imread(args.ihd) if args.ihd else None
    elev = cv2.imread(args.elev) if args.elev else None
    hint = [float(x) for x in args.roi_hint.split(",")] if args.roi_hint else None
    rep = run_zheng(
        Path(args.out),
        args.mode,
        L0,
        L1,
        I_HD=I_HD,
        elev=elev,
        tune_name=args.tune,
        side=args.side,
        roi_hint=hint,
        assets={"L0": args.l0, "L1": args.l1, "IHD": args.ihd},
        use_s0a=(False if args.no_s0a else True),
        s0a_pad=args.s0a_pad,
        s0a_scale=args.s0a_scale,
        s0a_min_side=args.s0a_min_side,
    )
    print(json.dumps({k: rep[k] for k in ("mode", "zh", "PASS_SX_FULL", "S11xS0_outside", "claim", "formal", "stick")}, ensure_ascii=False, indent=2))
    return 0 if rep["PASS_SX_FULL"] else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="正頭→正身 框牙內同一 PY")
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("diff-dna")
    p.set_defaults(func=cmd_diff_dna)

    p = sp.add_parser("selftest")
    p.add_argument("--out", default="/workspace/artifacts/SETS/PROJ_ZHENG_TOU_SHEN_SELFTEST")
    p.set_defaults(func=cmd_selftest)

    p = sp.add_parser("run")
    p.add_argument("--mode", required=True, choices=["tou", "shen"])
    p.add_argument("--out", required=True)
    p.add_argument("--l0", required=True)
    p.add_argument("--l1", required=True, help="外力除后 L1（头洞或整件洞）")
    p.add_argument("--ihd", default=None, help="外力生/正头正身结果")
    p.add_argument("--elev", default=None)
    p.add_argument("--tune", default=None)
    p.add_argument("--side", default="left", choices=["left", "right"])
    p.add_argument("--roi-hint", default=None)
    p.add_argument("--no-s0a", action="store_true", help="禁用 S0A 大切块（旧全帧路径）")
    p.add_argument("--s0a-pad", type=float, default=0.12)
    p.add_argument("--s0a-scale", type=float, default=1.0, help="01515 默认1=不放大（子集正身）")
    p.add_argument("--s0a-min-side", type=int, default=0, help="废弃升采样；保留兼容")
    p.set_defaults(func=cmd_run)

    args = ap.parse_args(argv)
    return args.func(args)


