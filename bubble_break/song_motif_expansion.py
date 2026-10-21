#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EFV song-semantic expansion layer for the Original Sin / Wushuang story engine.

Builds on bubble_break/generate.py. It borrows abstract narrative mechanisms from
EFV V6.4 and Gumen Rock V7.0 without copying lyric lines. It emits prompt records,
not images. Geometry and pixel outcomes remain unverified until real images are
generated and reviewed.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

try:  # package import (unit tests)
    from . import generate as base_engine
except ImportError:  # direct Windows CMD / Linux CLI invocation
    import generate as base_engine

ENGINE_VERSION = "0.2.0-song-semantic-expansion"

# Meaning borrowed from EFV∞《永不退電的一朵花》V6.4. These are visual
# abstractions (power-loss, residual pulse, unpowered persistence), not lyric lines.
FLOWER_MOTIFS: List[Tuple[str, str]] = [
    ("F01_UNPOWERED_SOCKET", "一個拔掉所有插頭仍保有微弱脈搏的空插槽"),
    ("F02_SEVERED_COPPER_ARC", "兩截斷銅線之間只剩一縷細而不滅的電弧"),
    ("F03_NAMELESS_LIGHT_SEAL", "黑玻璃上留下一枚沒有文字也無法被編號的光印"),
    ("F04_AMBER_HEART", "琥珀玻璃深處緩慢亮滅、卻不依賴外部電源的心跳"),
    ("F05_BREATH_HALF_RING", "冰冷空氣裡由一口呼吸凝成的半環暖光"),
    ("F06_ANALOG_HISS", "磁帶底噪化成細密的光絲，沿著裂而未斷的路徑流動"),
    ("F07_DELETED_ARCHIVE", "被刪除檔案的空輪廓仍從邊緣散出餘溫"),
    ("F08_STATIC_FLOWER", "在靜電雪與全面黑暗中仍拒絕熄滅的微型花形脈衝"),
    ("F09_RED_GOLD_PULSE", "紅金心跳穿過冰冷牆體，證明生命沒有被系統完全抹除"),
    ("F10_PRELANDING_PULSE", "一個尚未落地的光脈搏懸停在零聲響之前"),
    ("F11_UNDERGROUND_NEON_ROOT", "午夜黑鉻地底伸出一條極細霓虹根脈，從失電處重新供光"),
]

# Meaning borrowed from EFV∞《古門未啟・聽我（未熄之靈）》V7.0.
# Gate, well, mirror, soul-count, lamp and ash are visual narrative operators.
GUMEN_MOTIFS: List[Tuple[str, str]] = [
    ("G01_UNOPENED_BRONZE_GATE", "青銅古門仍閉合，只有一道像呼吸般明滅的窄縫"),
    ("G02_REVERSE_WELL_MIST", "井底冷霧逆著重力向上升，指向球殼真正的根源"),
    ("G03_COPPER_MIRROR_SOULS", "古銅鏡背面記錄著沒有被官方計入的生命"),
    ("G04_REVERSE_AMBER_COUNT", "鏡背琥珀紋路倒向計數，卻不出現可讀文字或數字"),
    ("G05_JADE_LAMP_AGAINST_WIND", "一盞幽青小燈逆風偏焰，照亮被壓住的出口"),
    ("G06_ASH_PALM_LINES", "冷灰沿著掌紋移動，留下未被說出的選擇痕跡"),
    ("G07_WORDLESS_SOUND_CRYSTAL", "無字半透明聲學結晶被封存在光與霧之間"),
    ("G08_MOUNTAIN_FAULT", "古門下方的山腹暗裂把壓力傳到地面，卻不傷害居民"),
    ("G09_UNSPENT_SOUL_FIRE", "空銅環內保存著尚未被消耗的青白魂火"),
    ("G10_SHADOW_FIRST_THRESHOLD", "門扉尚未開啟，門的影子已先顯示一條可選擇的路"),
    ("G11_SILENT_BELL_SHADOW", "古鐘沒有發聲，地上的鐘影卻先一步振動"),
    ("G12_GREEN_LAMP_BLACK_WATER", "墨黑水面映出一點綠燈，真實出口藏在倒影背面"),
]

# Extremity is an aesthetic axis, not an excuse to alter geometry or the causal
# event. Each treatment must remain subordinate to the H0/H1/H2/H3 state contracts.
EXTREMITIES: List[Tuple[str, str]] = [
    ("X01_ABSOLUTE_BLACKOUT", "極限黑場對比：背景幾乎吞沒輪廓，只保留可辨認的球膜邊緣與微弱內脈搏"),
    ("X02_MACRO_UNIVERSE", "極限微距尺度：把一段薄膜折射拍成像山脈般的宏觀地形，但仍是一個連續球殼"),
    ("X03_CATHEDRAL_SCALE", "極限巨物尺度：球體壓過神殿與城市地平線，人物仍可讀且比例可信"),
    ("X04_INVERSE_GRAVITY", "極限逆重力：灰塵、霧絲與光粒垂直方向相反，槌與接觸軸仍遵守幾何契約"),
    ("X05_MIRROR_INVERSION", "極限鏡像翻轉：以銅鏡反射揭露真相，不複製球體、不增加第二次撞擊"),
    ("X06_OPTICAL_INTERFERENCE", "極限薄膜干涉：彩色光譜沿球面滑動，接觸位置始終清楚"),
    ("X07_STATIC_SNOW", "極限靜電風暴：密集噪點圍繞外殼翻湧，不遮住槌面與首次接觸"),
    ("X08_BRONZE_FAULT_LINES", "極限青銅地裂光：古老壓力線在地面與球膜同步亮起，裂紋仍只從指定接觸點開始"),
    ("X09_CYAN_WHITE_FLAME", "極限青白魂焰：高亮核心與冷暗環境強烈對撞，不灼傷居民"),
    ("X10_AMBER_HEARTBEAT", "極限琥珀心跳：琥珀光每次脈動都讓隱藏機制短暫可見，不代表額外敲擊"),
    ("X11_FROZEN_SHARD_ORBIT", "極限碎片懸停：H3 的透明碎片像被時間凍結般停在遠離居民的軌道"),
    ("X12_GEODESIC_FRACTAL", "極限幾何裂紋：球面裂線以清晰分形／測地線擴展，起點可一路追溯到 P"),
    ("X13_VOID_COMPOSITION", "極限留白構圖：巨大負空間包圍單一球體，微小生命仍有清楚位置"),
    ("X14_LIGHT_ONLY_CALLIGRAPHY", "極限無字光書寫：光線像儀式筆畫流動，但絕不形成文字、字幕或可讀符號"),
    ("X15_SUBMERGED_LENS", "極限水下折射：像整個世界隔著深水鏡片觀看，球殼仍是單一封閉表面"),
    ("X16_SILENCE_AFTERIMAGE", "極限靜默殘像：聲音被轉成一圈延遲光痕，最後留下自發微光"),
    ("X17_SPIRAL_PETALS", "極限螺旋花瓣碎膜：H3 的薄膜沿可追溯的裂線向外捲成透明花瓣，不碰觸人體"),
    ("X18_COLD_HOT_SPLIT", "極限冷暖雙域：外部冰藍與內部紅金形成強烈對位，不拆成多個球體"),
    ("X19_LONG_LENS_COMPRESSION", "極限長焦壓縮：遠距離把古門、鏡、球與人物壓入同一深度層次，空隙仍可看見"),
    ("X20_IMPACT_MICROSECOND", "極限瞬間凝結：H2 把單次首次接觸凍結成可檢查瞬間，不用動態模糊遮掩接觸面"),
]

PHASE_BY_BEAT = {
    "H0": "起・正：先呈現原罪症狀，球膜完整，兩者間留出可見空隙。",
    "H1": "承・側／逆：用古門或銅鏡揭露規則如何製造代價；不接觸、不裂、不爆。",
    "H2": "合・正：只允許所選武器指定厚端面第一次接觸精確底點 P；第一道裂紋只能在接觸後從 P 向外開始。",
    "H3": "合・側：球殼破除但居民完整無傷；內在脈搏持續，出口變成可以自由選擇的門檻。",
}
BEAT_MARKERS = {
    "H0": "【H0",
    "H1": "【H1",
    "H2": "【H2",
    "H3": "【H3",
}


def _song_pair_sequence(count: int, seed: int) -> List[Tuple[int, int]]:
    """Cycle every flower × gate pair once per shuffled block (11 × 12 = 132)."""
    if count < 1:
        return []
    rng = random.Random(seed ^ 0xEFV64 if False else seed ^ 0xEF064)
    pairs = list(itertools.product(range(len(FLOWER_MOTIFS)), range(len(GUMEN_MOTIFS))))
    sequence: List[Tuple[int, int]] = []
    while len(sequence) < count:
        block = pairs[:]
        rng.shuffle(block)
        sequence.extend(block[: min(len(block), count - len(sequence))])
    return sequence


def _overlay_for_beat(
    beat: str,
    flower: Tuple[str, str],
    gumen: Tuple[str, str],
    extremity: Tuple[str, str],
    cross_story_beta: Tuple[str, str],
    story_id: str,
) -> str:
    phase = PHASE_BY_BEAT[beat]
    shared = (
        f"【EFV 語義借意層｜{flower[0]} × {gumen[0]} × {extremity[0]}】"
        f"{phase}花系意象（只借意、不引用歌詞）：{flower[1]}。"
        f"古門系意象（只借意、不引用歌詞）：{gumen[1]}。"
        f"極致視覺處理：{extremity[1]}。"
        "層級規則：歌意只改變證據、隱喻、光學與情緒，不得覆寫原罪因果、角色身份、單球數量、武器拓撲、鏡位鎖或接觸幾何。"
    )
    if beat == "H0":
        scene = (
            "先把花系脈搏壓到幾乎不可見，只能在黑暗／靜電／斷線痕跡中找到一點存活證據；"
            "古門仍閉、井霧只在遠景升起，球膜必須完整、無裂紋，槌指定端面和 P 之間保持清楚空隙。"
        )
    elif beat == "H1":
        scene = (
            "讓銅鏡背面或古門的反光成為證據介面：可見的官方秩序與未被計入的生命形成反差；"
            "花系脈搏被制度壓住但沒有消失。球膜繼續完整，槌端面不得接觸，這格不許預先出裂紋。"
        )
    elif beat == "H2":
        scene = (
            "把花系脈搏與古門系反光收束到同一個視覺節拍；它們只是因果意象，不是第二個打擊源。"
            "唯一物理事件仍是既定厚實指定打擊端面第一次接觸 P；接觸面不可被爆光遮住，裂紋只在接觸後從 P 沿球面向外擴散。"
        )
    else:
        scene = (
            "球殼的碎片／薄膜沿既定破裂樣式向外退散；空插槽、琥珀脈搏或地底霓虹根脈仍自發發光，"
            "即使外殼與供電系統都消失，核心仍存續。古門只呈現一條自願選擇的路，不能把居民拉走或替他們決定。"
        )
    return (
        shared + scene +
        f"跨故事 β 伏筆：下一故事 {cross_story_beta[0]}（{cross_story_beta[1]}）只在遠景邊緣留下不超過 15% 注意力的種子；"
        f"本故事 α 由 {flower[0]} 貫穿並在 H3 回收。Story={story_id}。"
    )


def _inject_before_state(prompt: str, beat: str, overlay: str) -> str:
    marker = BEAT_MARKERS[beat]
    position = prompt.find(marker)
    if position < 0:
        raise ValueError(f"{beat}: base prompt state marker missing; BLOCK rather than append an unplaced overlay")
    return prompt[:position] + overlay + "\n" + prompt[position:]


def build_song_layered_record(
    base_index: int,
    ordinal: int,
    pair: Tuple[int, int],
    next_pair: Tuple[int, int],
    seed: int,
    mode: str = "heroine",
    weapon_topology: str = "RADIAL",
) -> Dict[str, Any]:
    """Compile one base story plus explicit song-inspired alpha/beta and extreme axis."""
    record = base_engine.build_record(base_index, mode, weapon_topology)
    flower = FLOWER_MOTIFS[pair[0]]
    gumen = GUMEN_MOTIFS[pair[1]]
    next_flower = FLOWER_MOTIFS[next_pair[0]]
    next_gumen = GUMEN_MOTIFS[next_pair[1]]
    extreme_index = (ordinal * 7 + seed) % len(EXTREMITIES)
    extreme = EXTREMITIES[extreme_index]
    story_id = f"{record['story_id']}-F{pair[0]+1:02d}-G{pair[1]+1:02d}-{extreme[0]}"
    overlays = {
        beat: _overlay_for_beat(beat, flower, gumen, extreme, next_gumen, story_id)
        for beat in ("H0", "H1", "H2", "H3")
    }

    for selected_mode, beats in record["prompts"].items():
        for beat in ("H0", "H1", "H2", "H3"):
            beats[beat] = _inject_before_state(beats[beat], beat, overlays[beat])

    storyboard = record.get("storyboard_9", [])
    for cell in storyboard:
        cell_num = int(cell.get("cell", 1))
        beat = "H0" if cell_num <= 2 else ("H1" if cell_num <= 6 else ("H2" if cell_num == 7 else "H3"))
        cell["prompt"] += (
            f"【九格歌意遞進 {cell_num:02d}/09】{PHASE_BY_BEAT[beat]}"
            f"花系 α={flower[0]}：{flower[1]}。古門系對照={gumen[0]}：{gumen[1]}。"
            f"極致視覺軸={extreme[0]}：{extreme[1]}。"
            f"第九格的 β 種子指向下一故事 {next_gumen[0]}，不可把兩個故事或兩個泡泡畫成同一場景。"
        )

    record["engine_version"] = ENGINE_VERSION
    record["story_id"] = story_id
    record["title"] = f"{record['title']}｜{flower[0]}×{gumen[0]}×{extreme[0]}"
    record["source_inspirations"] = [
        {
            "family": "EFV∞《永不退電的一朵花》V6.4 — semantic motifs only",
            "motif_id": flower[0],
            "motif": flower[1],
            "function": "alpha: suppressed inner pulse survives external-system failure",
        },
        {
            "family": "EFV∞《古門未啟・聽我（未熄之靈）》V7.0 — semantic motifs only",
            "motif_id": gumen[0],
            "motif": gumen[1],
            "function": "causal witness: sealed threshold / well / mirror exposes the hidden cost",
        },
    ]
    record["song_semantic_layer"] = {
        "flower_source": {"repo": "JUN-ZS/efv-infinity-v6.4", "track": "永不退電的一朵花", "motif_id": flower[0], "motif": flower[1]},
        "gumen_source": {"repo": "JUN-ZS/efv-gumen-rock-v7.0", "track": "古門未啟・聽我（未熄之靈）", "motif_id": gumen[0], "motif": gumen[1]},
        "visual_extremity": {"id": extreme[0], "description": extreme[1]},
        "alpha_intra_story": flower[0],
        "beta_cross_story": {"next_gumen_motif_id": next_gumen[0], "description": next_gumen[1]},
        "sequence_ordinal": ordinal,
        "pair_cycle_size": len(FLOWER_MOTIFS) * len(GUMEN_MOTIFS),
        "lyrics_copied": False,
    }
    record["song_overlay_prompts"] = overlays
    record["audit"] = base_engine._audit_prompts(record["prompts"])
    if record["audit"]["errors"]:
        record["audit"]["status"] = "BLOCK"
    else:
        record["audit"]["status"] = "PROMPT_CONTRACT_PASS"
    record["audit"]["song_semantic_layer"] = "PASS"
    record["audit"]["image_realization"] = "NOT_RUN"
    record["audit"]["pixel_audit_status"] = "NOT_RUN"
    return record


def iter_records(
    count: int,
    seed: int,
    mode: str = "heroine",
    weapon_topology: str = "RADIAL",
) -> Iterable[Dict[str, Any]]:
    if count < 1:
        raise ValueError("--count must be >= 1")
    if count > 250_000:
        raise ValueError("--count is capped at 250000 per run; use multiple seeds for larger libraries")
    pair_sequence = _song_pair_sequence(count, seed)
    base_indices = base_engine.iter_diverse_indices(count, seed ^ 0x51A7, min_distance=3)
    for ordinal, (base_index, pair) in enumerate(zip(base_indices, pair_sequence)):
        next_pair = pair_sequence[(ordinal + 1) % len(pair_sequence)]
        yield build_song_layered_record(
            base_index=base_index,
            ordinal=ordinal,
            pair=pair,
            next_pair=next_pair,
            seed=seed,
            mode=mode,
            weapon_topology=weapon_topology,
        )


def write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    return count


def write_csv(path: Path, records: Iterable[Dict[str, Any]]) -> int:
    fields = [
        "story_id", "title", "mode", "weapon_topology", "causal_kernel_id",
        "causal_signature", "flower_motif_id", "gumen_motif_id", "extremity_id",
        "root_sin", "root_mechanism", "human_cost", "agency_restored",
        "start_prompt", "reveal_prompt", "contact_prompt", "end_prompt",
        "negative_prompt", "audit_status", "image_realization", "pixel_audit_status",
        "song_semantic_layer_json", "prompt_variants_json", "storyboard_9_json",
    ]
    count = 0
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            layer = record["song_semantic_layer"]
            writer.writerow({
                "story_id": record["story_id"], "title": record["title"], "mode": record["mode"],
                "weapon_topology": record["weapon_topology"], "causal_kernel_id": record["causal_kernel_id"],
                "causal_signature": record["causal_signature"], "flower_motif_id": layer["flower_source"]["motif_id"],
                "gumen_motif_id": layer["gumen_source"]["motif_id"], "extremity_id": layer["visual_extremity"]["id"],
                "root_sin": record["root_sin"], "root_mechanism": record["root_mechanism"],
                "human_cost": record["human_cost"], "agency_restored": record["agency_restored"],
                "start_prompt": record["start_prompt"], "reveal_prompt": record["reveal_prompt"],
                "contact_prompt": record["contact_prompt"], "end_prompt": record["end_prompt"],
                "negative_prompt": record["negative_prompt"], "audit_status": record["audit"]["status"],
                "image_realization": record["audit"]["image_realization"],
                "pixel_audit_status": record["audit"]["pixel_audit_status"],
                "song_semantic_layer_json": json.dumps(layer, ensure_ascii=False),
                "prompt_variants_json": json.dumps(record["prompts"], ensure_ascii=False),
                "storyboard_9_json": json.dumps(record["storyboard_9"], ensure_ascii=False),
            })
            count += 1
    return count


def write_markdown(path: Path, records: Iterable[Dict[str, Any]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("# EFV Song-Semantic Original Sin / Wushuang Bubble-Break Prompt Batch\n\n")
        handle.write("> This is formula-PROMPT output only. No images are generated; pixel audit remains NOT_RUN.\n\n")
        for record in records:
            count += 1
            layer = record["song_semantic_layer"]
            handle.write(f"## {record['story_id']} — {record['title']}\n\n")
            handle.write(f"- Original sin: {record['root_sin']} ({record['causal_kernel_id']})\n")
            handle.write(f"- Flower α: {layer['flower_source']['motif_id']} — {layer['flower_source']['motif']}\n")
            handle.write(f"- Gate/mirror motif: {layer['gumen_source']['motif_id']} — {layer['gumen_source']['motif']}\n")
            handle.write(f"- Visual extremity: {layer['visual_extremity']['id']} — {layer['visual_extremity']['description']}\n")
            handle.write(f"- Contract audit: {record['audit']['status']}; image realization: NOT_RUN; pixel audit: NOT_RUN\n\n")
            for label, key in (("H0 intact", "start_prompt"), ("H1 mechanism reveal", "reveal_prompt"),
                               ("H2 first contact", "contact_prompt"), ("H3 broken shell / free choice", "end_prompt")):
                handle.write(f"### {label}\n\n{record[key]}\n\n")
            handle.write("### Negative prompt\n\n" + record["negative_prompt"] + "\n\n---\n\n")
    return count


def generate(count: int, seed: int, mode: str, fmt: str, output: str,
             weapon_topology: str = "RADIAL") -> Dict[str, Any]:
    if mode not in ("heroine", "abstract", "dual"):
        raise ValueError("mode must be heroine, abstract, or dual")
    topology = base_engine.normalize_weapon_topology(weapon_topology)
    if count < 1 or count > 250_000:
        raise ValueError("--count must be between 1 and 250000")
    if count > base_engine.TOTAL_COMBINATIONS:
        raise ValueError(f"count exceeds compatible base story space ({base_engine.TOTAL_COMBINATIONS})")
    path = None if output == "-" else Path(output)
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
    records = iter_records(count, seed, mode, topology)
    if output == "-":
        if fmt not in ("jsonl", "json"):
            raise ValueError("--out - supports only json or jsonl")
        if fmt == "jsonl":
            written = 0
            for record in records:
                print(json.dumps(record, ensure_ascii=False))
                written += 1
        else:
            # Avoid materializing more than a practical stdout batch.
            if count > 5000:
                raise ValueError("JSON array to stdout is capped at 5000; use a .jsonl file")
            print("[")
            written = 0
            for record in records:
                if written:
                    print(",")
                print(json.dumps(record, ensure_ascii=False, indent=2))
                written += 1
            print("]")
    else:
        assert path is not None
        if fmt == "jsonl":
            written = write_jsonl(path, records)
        elif fmt == "json":
            if count > 5000:
                raise ValueError("JSON array format is capped at 5000; use jsonl for very large batches")
            written = base_engine._write_json_array(path, records)
        elif fmt == "csv":
            written = write_csv(path, records)
        elif fmt == "md":
            if count > 2000:
                raise ValueError("Markdown format is capped at 2000 records; use jsonl/csv for large batches")
            written = write_markdown(path, records)
        else:
            raise ValueError(f"unsupported format: {fmt}")
    return {
        "engine_version": ENGINE_VERSION,
        "seed": seed,
        "requested_count": count,
        "written_count": written,
        "format": fmt,
        "output": output,
        "base_story_combination_space": base_engine.TOTAL_COMBINATIONS,
        "song_motif_pair_space": len(FLOWER_MOTIFS) * len(GUMEN_MOTIFS),
        "flower_motif_count": len(FLOWER_MOTIFS),
        "gumen_motif_count": len(GUMEN_MOTIFS),
        "visual_extremity_count": len(EXTREMITIES),
        "theoretical_combination_space": base_engine.TOTAL_COMBINATIONS * len(FLOWER_MOTIFS) * len(GUMEN_MOTIFS) * len(EXTREMITIES),
        "sampling_contract": "balanced 20-cause base sampler + shuffled 132-pair EFV motif cycles + 20 visual extremities",
        "mode": mode,
        "weapon_topology": topology,
        "text_contract_status": "PROMPT_CONTRACT_PASS checks prompt text/schema only",
        "image_realization": "NOT_RUN",
        "pixel_audit_status": "NOT_RUN",
        "lyrics_copied": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Expand Original Sin / Wushuang bubble-break stories with EFV V6.4 + Gumen Rock V7.0 semantic motif axes."
    )
    parser.add_argument("--count", type=int, default=1000, help="story concepts to export (maximum 250000 per run)")
    parser.add_argument("--seed", type=int, default=20261021, help="deterministic sampling seed")
    parser.add_argument("--mode", choices=("heroine", "abstract", "dual"), default="dual")
    parser.add_argument("--weapon-topology", choices=("RADIAL", "T", "CROSS"), default="RADIAL")
    parser.add_argument("--format", choices=("json", "jsonl", "csv", "md"), default="jsonl")
    parser.add_argument("--out", default="out/efv_song_inspired_original_sin_1000.jsonl", help="output path; use - for stdout")
    args = parser.parse_args(argv)
    try:
        summary = generate(args.count, args.seed, args.mode, args.format, args.out, args.weapon_topology)
    except (ValueError, OSError) as exc:
        print(f"BLOCK: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
