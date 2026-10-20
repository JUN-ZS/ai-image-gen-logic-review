#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Original Sin / Wushuang Bubble-Break story-image prompt compiler.

Standard-library only. Generates text contracts, not rendered images. A PASS from
this script is not evidence that an image or video model obeyed the prompt.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

ENGINE_VERSION = "0.1.0"

# Semantic story kernels: distilled themes, not verbatim song lyrics.
SIN_PROFILES = [
 {"id":"SIN01","name":"Perfect Safety","promise":"no one will ever be hurt again","mechanism":"the membrane silently removes every memory that might produce grief, disagreement, or refusal","cost":"residents remain physically safe but cannot remember who they loved or why they once objected","choice":"restore memories without prescribing what residents must do with them","evidence":"identical smiles coexist with hands reaching toward erased photographs"},
 {"id":"SIN02","name":"Predestined Peace","promise":"every life will follow the safest forecast","mechanism":"probability lanes bend each resident toward one preselected future and close every alternative route","cost":"the shell calls obedience harmony and treats every unpredicted choice as a defect","choice":"let residents choose different futures, including uncertain ones","evidence":"thousands of luminous paths collapse into one corridor, while a single unscripted footprint remains"},
 {"id":"SIN03","name":"Purity Without Difference","promise":"a flawless society can be built by filtering out every irregularity","mechanism":"the sphere sorts people into invisible ranks and hides those it labels imperfect","cost":"the hidden residents are not dangerous; the classification system is the source of the fear","choice":"break the ranking rule rather than punish the people ranked by it","evidence":"the shell's bright outer layer is immaculate while its inner surface is covered in suppressed names"},
 {"id":"SIN04","name":"Memory Quarantine","promise":"the past can be sealed away so the present stays clean","mechanism":"the shell stores collective memories as amber fragments and feeds on residents' amnesia","cost":"the community cannot recognize inherited harm or decide how to repair it","choice":"return the fragments with room for truth, mourning, and accountability","evidence":"amber shards orbit the sphere, each casting a different shadow of the same event"},
 {"id":"SIN05","name":"Silence Tax","promise":"silence will prevent conflict","mechanism":"every unspoken objection becomes a pressure ring that thickens the membrane","cost":"the quietest residents pay the greatest price and the shell mistakes fear for consent","choice":"release suppressed voices without forcing anyone to speak","evidence":"concentric rings tighten whenever a resident opens their mouth, yet a tiny breath-light survives"},
 {"id":"SIN06","name":"Manufactured Scarcity","promise":"strict rationing is the only way to keep the world alive","mechanism":"the shell hides abundant light, water, and space behind artificial scarcity gauges","cost":"neighbors compete for resources the system is withholding from them","choice":"open the membrane and let residents negotiate shared access themselves","evidence":"the supposedly empty reservoir is visibly full on the inside of a mirrored wall"},
 {"id":"SIN07","name":"Permanent Emergency","promise":"the alarm must never stop because danger might return","mechanism":"the shell manufactures phantom threats; each panic wave reinforces its own containment field","cost":"residents can no longer distinguish evidence from warning","choice":"end the alarm cycle and let people assess real risks together","evidence":"red warning strobes cast shadows, but every shadow points toward an absent attacker"},
 {"id":"SIN08","name":"Emotional Sterilization","promise":"removing intense feelings will remove suffering","mechanism":"the shell drains color and heartbeat from every feeling, storing them as a rotating core","cost":"pain fades, but tenderness, curiosity, and courage fade with it","choice":"return the full emotional spectrum, not a forced happy ending","evidence":"colorless faces stand beside a bright core made of stolen red-gold pulse fragments"},
 {"id":"SIN09","name":"Identity Ownership","promise":"a single authorized name makes society legible","mechanism":"the shell replaces private names with serial marks and absorbs anyone who changes theirs","cost":"residents cannot describe who they have become or whom they choose to love","choice":"return names as self-chosen, changeable declarations","evidence":"blank nameplates orbit the membrane and one light-mark refuses to vanish"},
 {"id":"SIN10","name":"Perfect Replay","promise":"repeating the best day forever will prevent regret","mechanism":"the shell resets time just before any resident can make a consequential choice","cost":"every apparent reunion is a loop; no relationship can progress or heal","choice":"allow time to move forward even when the next day is unknown","evidence":"the same falling leaf appears at several impossible positions around the sphere"},
 {"id":"SIN11","name":"Inherited Guilt","promise":"descendants must pay for an unexamined ancient wrong","mechanism":"the shell turns inherited guilt into a gravity field that pins every generation in place","cost":"living people are punished for a history they were never allowed to examine","choice":"keep the evidence of the past, end automatic punishment, and choose repair freely","evidence":"old bronze seals weigh on the shell while living hands inside are open and unchained"},
 {"id":"SIN12","name":"Weaponized Protection","promise":"the protected must never cross the boundary","mechanism":"the shell redirects every exit attempt back toward its center and calls the recoil protection","cost":"a shelter becomes a prison without changing its comforting appearance","choice":"open a real exit and let each resident decide whether to leave or stay","evidence":"a door-shaped absence is visible from inside but becomes a solid mirror from outside"},
 {"id":"SIN13","name":"Algorithmic Worth","promise":"a score can measure the value of every life","mechanism":"the shell moves residents according to an invisible score and converts low scores into dimness","cost":"people mistake a changing measurement for a permanent identity","choice":"remove the coercive score while preserving voluntary evidence and personal responsibility","evidence":"rank lines crawl across the membrane but cannot attach to residents' unmarked hands"},
 {"id":"SIN14","name":"Infinite Productivity","promise":"rest is a defect that can be optimized away","mechanism":"the membrane converts every pause into energy and prevents residents from stopping","cost":"the system survives by consuming the people it claims to empower","choice":"give time back to residents, including the right to rest without justification","evidence":"a giant clock has no hands, while exhausted light threads are pulled into the shell's equator"},
 {"id":"SIN15","name":"Fear of the Outside","promise":"everything beyond the wall is monstrous","mechanism":"the membrane distorts the outside into threatening silhouettes and erases contrary evidence","cost":"residents fear a world they have never been allowed to inspect","choice":"reveal the outside honestly and allow a voluntary, reversible first step","evidence":"the terrifying silhouettes have no bodies; their shapes are cast by the shell's own ribs"},
 {"id":"SIN16","name":"Borrowed Immortality","promise":"no one will be lost if nothing is allowed to change","mechanism":"the shell freezes residents in crystal snapshots and prevents growth, aging, and farewell","cost":"preservation becomes a refusal to let a life continue","choice":"release time and let change belong to the people living through it","evidence":"within the crystal, one tiny flower has continued growing and cracked its own reflection"},
 {"id":"SIN17","name":"Compulsory Forgiveness","promise":"harmony requires every wound to be declared healed","mechanism":"the shell erases visible scars before those harmed can describe what happened","cost":"the system protects its reputation instead of protecting injured people","choice":"restore the right to speak, set boundaries, seek repair, or decline reconciliation","evidence":"the polished membrane reflects an unscarred face while the real shadow carries the missing mark"},
 {"id":"SIN18","name":"Ownership of Attention","promise":"constant visibility will make everyone matter","mechanism":"the shell turns gaze and applause into fuel and dims anyone who chooses privacy","cost":"residents perform for the cage and lose the ability to be unobserved","choice":"return privacy and attention as choices rather than obligations","evidence":"thousands of eye-like reflections face inward, but one dark window remains peacefully unlit"},
 {"id":"SIN19","name":"One-Truth Archive","promise":"a single official story will end confusion","mechanism":"the shell flattens conflicting testimonies into one polished mirrored account","cost":"differences in memory are treated as threats rather than evidence to examine","choice":"let distinct accounts coexist and be investigated without forced consensus","evidence":"the mirrored sphere shows one image from the front and many truthful angles at its edge"},
 {"id":"SIN20","name":"Boundary as Original Sin","promise":"the line itself can decide who belongs","mechanism":"the shell treats its own border as moral law and converts crossings into visible faults","cost":"people are divided by an arbitrary surface that pretends to be nature","choice":"make the boundary negotiable and preserve each person's right to consent","evidence":"a fine luminous seam encircles the world but has no foundation, lock, or support"},
]

SHELL_FORMS = [
 ("SHELL01","an ultra-thin iridescent soap-film sphere with oil-slick interference colors"),
 ("SHELL02","a transparent amber sphere with layered fossil-like memory inclusions"),
 ("SHELL03","a crystal-geodesic membrane with thousands of precise triangular facets"),
 ("SHELL04","a clear water sphere held together by a razor-thin surface-tension skin"),
 ("SHELL05","a black-glass sphere that bends background stars without becoming opaque"),
 ("SHELL06","a mirrored silver sphere made of overlapping scales, each reflecting a different resident"),
 ("SHELL07","a translucent ice membrane with trapped air veins and blue-white refraction"),
 ("SHELL08","a smoky pearl sphere whose closed surface is visible where light grazes it"),
 ("SHELL09","a ceramic-white shell with hairline gold seams, pristine until impact"),
 ("SHELL10","a holographic grid sphere whose luminous nodes connect through a continuous transparent skin"),
 ("SHELL11","a thin bronze-and-glass membrane with engraved concentric containment rings"),
 ("SHELL12","a dark liquid-metal sphere with a smooth, continuous reflective surface"),
 ("SHELL13","a giant bubble made of layered rainbow film, each layer carrying a distinct optical phase"),
 ("SHELL14","a matte translucent mineral sphere with a bright inner horizon and a visible outer membrane"),
]
ENVIRONMENTS = [
 ("ENV01","a drowned archive where book spines float upright in still water"),
 ("ENV02","a ruined underground transit hall with rails converging toward the sphere"),
 ("ENV03","a salt desert at eclipse, the ground split into enormous polygonal plates"),
 ("ENV04","a suspended temple above a bottomless well of silver mist"),
 ("ENV05","an abandoned orbital greenhouse with broken ribs and distant stars"),
 ("ENV06","a midnight industrial city with unlit towers and thin copper conduits"),
 ("ENV07","a wind-scoured mountain pass with ancient gate stones and drifting ash"),
 ("ENV08","a cathedral-sized machine room where every gear has stopped one tooth before alignment"),
 ("ENV09","a flooded library beneath a glass roof, moonlight refracted through black water"),
 ("ENV10","a white void containing only a horizon line, a shadow, and the enclosed world"),
 ("ENV11","a cracked lunar plain above a blue planet, with dust suspended in low gravity"),
 ("ENV12","an overgrown observatory where vines wrap abandoned brass instruments"),
 ("ENV13","a ruined fairground whose silent bulbs light one by one without a power source"),
 ("ENV14","a deep-sea trench with distant bioluminescent organisms outside the membrane"),
]
SCALES = [
 ("SCALE01","a 0.6-metre memory-bubble rendered as a monumental 100mm macro landscape"),
 ("SCALE02","a human-sized sphere enclosing a small group of living residents"),
 ("SCALE03","an 8-metre sphere suspended inside a broken industrial chamber"),
 ("SCALE04","a 40-metre sphere floating above a deserted plaza"),
 ("SCALE05","a cathedral-dome sphere enclosing an entire neighborhood square"),
 ("SCALE06","a city-scale sphere whose curvature hides its horizon behind cloud bands"),
 ("SCALE07","a mountain-scale sphere whose lower arc rises above the ridgeline"),
 ("SCALE08","an orbital sphere enclosing a habitat ring against a planetary limb"),
 ("SCALE09","a moon-scale containment sphere with a clearly readable six-o'clock underside"),
 ("SCALE10","a universe-in-miniature sphere whose star field is bounded by one continuous membrane"),
]
HAMMER_FINISHES = [
 ("HAM01","blackened meteor-iron with narrow bronze seams"),
 ("HAM02","brushed silver steel with blue-white stress glints"),
 ("HAM03","oxidized copper with a warm amber core"),
 ("HAM04","dark basalt-metal with thin red-gold circuit veins"),
 ("HAM05","pale ceramic armor over a dense steel striking core"),
 ("HAM06","rainbow-titanium facets that refract without changing head geometry"),
 ("HAM07","ancient bronze engraved with non-text geometric rings"),
 ("HAM08","obsidian and cold silver, with no organic deformation"),
 ("HAM09","matte gunmetal carrying a single persistent electric pulse"),
 ("HAM10","clear crystal armor around a visibly dense metallic core"),
]
FRACTURES = [
 ("FRAC01","thin radial cracks travel along geodesic paths like a precisely opened ice crystal"),
 ("FRAC02","the film peels into enormous translucent petals, each fragment moving outward from the underside"),
 ("FRAC03","mirror scales separate into a controlled spiral of harmless reflective slivers"),
 ("FRAC04","the liquid membrane opens as a clean expanding ring, then turns into suspended droplets"),
 ("FRAC05","grid nodes go dark outward in a visible causal wave, leaving residents untouched"),
 ("FRAC06","the shell divides into concentric transparent layers that drift apart without a blast wave"),
 ("FRAC07","crystal facets detach one by one along a radial propagation front, like a mapped constellation"),
 ("FRAC08","the smoky surface unthreads into luminous filaments that unravel away from residents"),
 ("FRAC09","ceramic-gold seams unzip from the contact point and release tiny light grains"),
 ("FRAC10","the spherical boundary becomes suspended glass ribbons whose trajectories trace back to one origin"),
 ("FRAC11","a prismatic rupture wave crosses the membrane while the inner volume remains calm"),
 ("FRAC12","the spherical boundary folds outward into a toroidal halo, leaving an open passage rather than an explosion"),
]
CAMERAS = [
 ("CAM01","locked frontal 35mm anamorphic wide shot, low camera slightly below the sphere's centerline"),
 ("CAM02","locked 50mm eye-level shot with the sphere center and exact bottom point unobstructed"),
 ("CAM03","locked 85mm macro-compressed shot, contact geometry and distant residents in layered focus"),
 ("CAM04","locked three-quarter 45-degree shot with parallax but no viewpoint change between paired frames"),
 ("CAM05","locked 24mm monumental low-angle shot with vertical architecture as alignment guides"),
 ("CAM06","locked side-on orthographic-like shot with minimal perspective distortion"),
 ("CAM07","locked silhouette shot with a clear negative-space gap below the intact sphere"),
 ("CAM08","locked 70mm telephoto shot through a foreground ring, contact point unobstructed"),
 ("CAM09","locked 28mm wide shot with visible horizon, ground plane, sphere centerline, and lower contact point"),
 ("CAM10","locked top-front three-quarter shot angled to show the lower pole and residents inside"),
 ("CAM11","locked 100mm extreme macro showing both spherical curvature and hammer end-face"),
 ("CAM12","locked deep-focus 40mm shot using architecture as straight vertical and horizontal references"),
]
PALETTES = [
 ("PAL01","cold silver, electric cyan, and one restrained amber life-signal"),
 ("PAL02","oxidized bronze, ink black, and pale jade mist"),
 ("PAL03","ultraviolet glass, white-hot rim light, and deep ocean blue"),
 ("PAL04","crimson warning light resolving into warm gold after the breach"),
 ("PAL05","moon-white, graphite, and spectral rainbow interference"),
 ("PAL06","salt white, burnt umber, and a thin red-gold pulse"),
 ("PAL07","deep-sea teal, black glass, and bioluminescent pinpoints"),
 ("PAL08","frost blue, smoked chrome, and a soft copper sunrise"),
 ("PAL09","monochrome charcoal with tiny color fragments released only after impact"),
 ("PAL10","saturated cobalt, pale amber, and iridescent clear glass"),
 ("PAL11","matte bone white, antique brass, and hard black shadows"),
 ("PAL12","eclipse violet, silver dust, and a green-lamp point of hope"),
]
AFTERGLOWS = [
 ("AFTER01","survivors open their hands and choose separate paths; no one orders where they go"),
 ("AFTER02","one resident kneels to remember a name while another voluntarily reaches toward a companion"),
 ("AFTER03","the group looks toward the real horizon for the first time, with fear and curiosity both allowed"),
 ("AFTER04","residents help one another stand, then pause before an unguarded open threshold"),
 ("AFTER05","a small silhouette points toward the outside while adults retain the option to stay"),
 ("AFTER06","lost memories return as gentle reflections, not as commands or compulsory forgiveness"),
 ("AFTER07","the residents turn off the false alarm themselves and listen to the environment"),
 ("AFTER08","the first freely chosen light is lit by a resident, not by the Boundary Walker"),
 ("AFTER09","residents begin an honest public record with multiple distinct reflections"),
 ("AFTER10","the group separates from the broken membrane and stands unharmed amid harmless drifting light"),
]
FLOWER_MOTIFS = [
 "one unpowered socket holding a faint pulse",
 "a hairline electric arc bridging two severed copper ends",
 "glassy rain-window reflections arranged like a nameless seal",
 "warm breath condensed into a half-ring in cold air",
 "analog tape hiss visualized as fine luminous filaments",
 "a deleted archive folder whose edge still emits warmth",
 "a small flower-shaped pulse that refuses to go dark",
 "a red-gold heartbeat travelling through a cold wall",
 "a flower-like light signature surviving in static",
 "a soft pulse suspended one instant before it lands",
 "a thin neon vein beneath midnight metal",
]
GUMEN_MOTIFS = [
 "an unopened bronze gate with a single breathing seam",
 "mist rising against gravity from the bottom of an ancient well",
 "an old copper mirror whose reverse side records uncounted lives",
 "a small jade lamp whose flame leans into the wind",
 "iron feathers passing over abandoned roofs",
 "a cracked-moon-like silver blade in the sky",
 "amber soul-fire held inside an empty bronze ring",
 "a silent bell whose shadow vibrates before the bell moves",
 "a line of ash glowing beneath an old stone wall",
 "a paper boat carrying one drop of ink through a dark current",
 "a green lamp reflected inside black water",
 "a threshold whose shadow opens before the door does",
]
PHASES = [
 ("01","起・正","O_Front","0 degrees","symptom and world-rule"),
 ("02","起・側","O_Side","45 degrees","trace the shell's behavior"),
 ("03","承・側","O_Side","75 degrees","show the human cost"),
 ("04","承・正＋alpha","O_Front","15 degrees","plant the intra-story seed"),
 ("05","轉・側","O_Side","60 degrees","break the apparent logic"),
 ("06","轉・逆","O_Inv","180 degrees","reveal the hidden causal inversion"),
 ("07","合・正","O_Front","0 degrees","the single exact contact event"),
 ("08","合・側","O_Side","65 degrees","show harmless release and agency"),
 ("09","跨段門＋beta","O_Inv","180/360 degrees","seed a different next story"),
]
AXES = [
 ("sin",SIN_PROFILES), ("shell",SHELL_FORMS), ("environment",ENVIRONMENTS),
 ("scale",SCALES), ("hammer",HAMMER_FINISHES), ("fracture",FRACTURES),
 ("camera",CAMERAS), ("palette",PALETTES), ("afterglow",AFTERGLOWS),
]
RAW_COMBINATIONS = 1
for _, choices in AXES:
    RAW_COMBINATIONS *= len(choices)

# A shell's material has to support its rupture behavior. This blocks incoherent
# pairings rather than merely changing color words between otherwise identical prompts.
COMPATIBLE_FRACTURES = {
    "SHELL01": {"FRAC02","FRAC04","FRAC08","FRAC11","FRAC12"},
    "SHELL02": {"FRAC01","FRAC06","FRAC07","FRAC09","FRAC10"},
    "SHELL03": {"FRAC01","FRAC06","FRAC07","FRAC10","FRAC11"},
    "SHELL04": {"FRAC02","FRAC04","FRAC08","FRAC11","FRAC12"},
    "SHELL05": {"FRAC01","FRAC03","FRAC06","FRAC07","FRAC10"},
    "SHELL06": {"FRAC03","FRAC06","FRAC07","FRAC10","FRAC11"},
    "SHELL07": {"FRAC01","FRAC06","FRAC07","FRAC09","FRAC11"},
    "SHELL08": {"FRAC02","FRAC08","FRAC11","FRAC12"},
    "SHELL09": {"FRAC01","FRAC06","FRAC07","FRAC09","FRAC10"},
    "SHELL10": {"FRAC05","FRAC06","FRAC11","FRAC12"},
    "SHELL11": {"FRAC01","FRAC03","FRAC06","FRAC09","FRAC10"},
    "SHELL12": {"FRAC03","FRAC04","FRAC08","FRAC11","FRAC12"},
    "SHELL13": {"FRAC02","FRAC04","FRAC06","FRAC08","FRAC11","FRAC12"},
    "SHELL14": {"FRAC01","FRAC06","FRAC07","FRAC09","FRAC10"},
}
_nonpaired_axes = 1
for axis_index, (_, choices) in enumerate(AXES):
    if axis_index not in (1, 5):
        _nonpaired_axes *= len(choices)
TOTAL_COMBINATIONS = _nonpaired_axes * sum(len(v) for v in COMPATIBLE_FRACTURES.values())


def _decode_index(index: int) -> Tuple[int, ...]:
    if index < 0 or index >= RAW_COMBINATIONS:
        raise ValueError("combination index out of range")
    out = [0] * len(AXES)
    rest = index
    for pos in range(len(AXES) - 1, -1, -1):
        radix = len(AXES[pos][1])
        out[pos] = rest % radix
        rest //= radix
    return tuple(out)


def _select_by_index(index: int) -> Dict[str, Tuple[str, str]]:
    digits = _decode_index(index)
    return {name: choices[digit] for (name, choices), digit in zip(AXES, digits)}


def _hamming(a: Sequence[int], b: Sequence[int]) -> int:
    return sum(1 for x, y in zip(a, b) if x != y)


def _is_compatible(digits: Sequence[int]) -> bool:
    shell_id = SHELL_FORMS[digits[1]][0]
    fracture_id = FRACTURES[digits[5]][0]
    return fracture_id in COMPATIBLE_FRACTURES[shell_id]


def iter_diverse_indices(count: int, seed: int, min_distance: int = 3) -> Iterable[int]:
    """Deterministic sampling without duplicate combinations, with a local diversity check."""
    if count < 1:
        raise ValueError("count must be >= 1")
    if count > TOTAL_COMBINATIONS:
        raise ValueError(f"count exceeds combination space ({TOTAL_COMBINATIONS})")
    rng = random.Random(seed)
    seen = set()
    accepted: List[Tuple[int, ...]] = []
    distance = min_distance if count < TOTAL_COMBINATIONS * 0.4 else 0
    while len(accepted) < count:
        index = rng.randrange(TOTAL_COMBINATIONS)
        if index in seen:
            continue
        seen.add(index)
        digits = _decode_index(index)
        if not _is_compatible(digits):
            continue
        if distance and any(_hamming(digits, old) < distance for old in accepted[-24:]):
            if len(seen) < min(TOTAL_COMBINATIONS, count * 60):
                continue
            distance = max(0, distance - 1)
        accepted.append(digits)
        yield index


def _stable_id(selected: Dict[str, Tuple[str, str]]) -> str:
    signature = "|".join(f"{key}:{selected[key][0]}" for key, _ in AXES)
    return "OSBB-" + hashlib.sha256(signature.encode("utf-8")).hexdigest()[:12].upper()


def _mode_anchor(mode: str) -> str:
    if mode == "heroine":
        return (
            "角色鎖 λ_H=1：同一位東亞女性 Boundary Walker，深棕色中分長髮、左眼下方一顆細小清楚的痣；"
            "同一張臉、同一服裝剪影、同一身高比例與手部數量，無換臉、無複製女主。"
            "她打破的是封存規則，不是受困居民。"
        )
    return (
        "角色鎖 λ_H=0：不出現前景女主或清晰主角臉；以四頭戰錘、垂直導向機構與球殼幾何作為畫面主體，"
        "驅動力沿受約束的垂直導軌向上傳遞。泡內居民仍以可辨的完整人物或剪影呈現，"
        "確保其存活與選擇不能被純抽象畫面遮掉。"
    )


GEOMETRY_LOCK = (
    "【不可改寫的三維幾何契約】世界座標 Y 軸向上；球膜球心 C=(0,R,0)，半徑 R，球底唯一目標點 "
    "P=C+(0,-R,0)=(0,0,0)，即球體精確 6 點鐘位置。該點球膜外法線 n_target=(0,-1,0)；"
    "戰錘向上打擊端面的法線 n_hammer=(0,+1,0)=-n_target；打擊速度 v=(0,+V,0), V>0。"
    "戰錘是唯一一把完整、真正三維的四頭十字戰錘：四個錘頭有實際厚度與可辨前後深度，固定連接在同一剛性錘身，"
    "沒有獨立旋轉、分離、複製或軟化。只有上端厚實平整的指定打擊端面可以首先接觸球膜底點 P；"
    "側面錘頭、錘柄、握柄、人物身體及任何其他物件均不得先碰球膜。"
    "H0/H1 必須保留可見空隙與完整無裂球膜；H2 才能首次接觸；裂紋必須由 P 起始並沿球面向外傳播。"
    "被擊中的是封存球膜／拘束機制，不是居民；球內的人與承載面不得被錘擊、裂片、衝擊波或崩落物傷害。"
)
SCENE_LOCK = (
    "【首尾幀同一場景鎖】16:9、1920×1080、單一完整電影畫面，不是拼貼、不含字幕/標籤/浮水印。"
    "配對 H0 與 H3 必須使用同一攝影機位置、同一鏡頭焦距、同一地平線、同一球心投影位置、"
    "同一環境地標、同一主角身分、同一錘頭尺寸與剛體朝向、同一主光方向；只改變事件狀態與殼體完整度。"
    "保持泡殼曲率、球心、6 點鐘接觸座標與上下方向一致；不得為了戲劇效果偷換鏡位或移動接觸點。"
)
NEGATIVE_PROMPT = (
    "禁止：側面橫掃、由上往下劈、錘柄碰球、錘頭側面先碰球、球膜在接觸前先裂、裂紋從側面或球頂開始、"
    "四頭戰錘變成二頭/一頭/多把錘、錘頭與錘柄分離、軟柄彎曲、錘頭自行旋轉、接觸點飄移、人物被打中、"
    "居民受傷或死亡、內部建築被爆炸摧毀、碎片向人群高速射擊、血腥、把受困者畫成罪犯、"
    "只畫爆炸不畫球膜、只畫光效卻沒有完整三維球體、雙重女主、額外肢體/手指、文字、字幕、標誌、浮水印。"
)


def _alpha_beta(index: int) -> Tuple[str, str]:
    flower = FLOWER_MOTIFS[index % len(FLOWER_MOTIFS)]
    gumen = GUMEN_MOTIFS[(index * 7 + 3) % len(GUMEN_MOTIFS)]
    return (flower, gumen) if index % 2 == 0 else (gumen, flower)


def _prompt_for_beat(
    beat: str, selected: Dict[str, Tuple[str, str]], mode: str,
    alpha: str, beta: str, camera_line: str
) -> str:
    sin = selected["sin"][1]
    shell = selected["shell"][1]
    fracture = selected["fracture"][1]
    env = selected["environment"][1]
    scale = selected["scale"][1]
    hammer = selected["hammer"][1]
    palette = selected["palette"][1]
    after = selected["afterglow"][1]
    base = (
        f"16:9 1920×1080 電影級單幀，極致可讀的三維空間、真實光學、清晰前中後景。{camera_line}"
        f"{_mode_anchor(mode)}故事核：{sin['name']}。{sin['mechanism']}。"
        f"場景：{env}；尺度：{scale}；球殼：{shell}；色彩：{palette}。"
        f"戰錘外觀：{hammer}，但固定四頭結構、剛性長柄與厚實平整打擊端面不得改形。"
        f"{SCENE_LOCK}{GEOMETRY_LOCK}"
        f"【55/30/15敘事資訊預算，不是像素權重】55%鎖定本幀主要狀態；30%只保留經鏡位轉換的前一狀態殘影；"
        f"15%預埋下一狀態伏筆 α={alpha}、β={beta}。不得因此複製人物、預先生成裂紋或改變實際接觸座標。"
    )
    if beat == "H0":
        state = (
            "【H0 起始錨點：封存仍完整】球膜完整、封閉、乾淨，無預存裂紋、無爆裂、無缺口。"
            "所有居民仍在膜內，身體完整、沒有受傷；透過球膜可辨認他們被錯誤規則限制的日常。"
            "戰錘停在球底 P 正下方，指定向上打擊端面與 P 之間有清楚、連續、肉眼可見的空隙；"
            "不得接觸球殼，錘柄垂直剛直，四個錘頭全部可判讀為同一把完整三維器物。"
            f"以可見症狀暗示原罪：{sin['evidence']}。遠景預埋段內伏筆 α：{alpha}。"
            "情緒是即將作出選擇前的壓抑與清醒，而不是已經發生爆炸。"
        )
    elif beat == "H1":
        state = (
            "【H1 揭露：看見機制，不先破壞】球膜依然完整且完全沒有裂紋，戰錘端面仍與球底 P 保持可見空隙。"
            f"畫面用內外對照呈現代價：{sin['cost']}；居民仍活著，卻被錯誤規則限制。"
            f"段內伏筆 α={alpha} 在球膜局部折射／倒影裡出現，但不是裂紋，不是接觸，不是爆炸。"
            "情感轉折是 Boundary Walker 先辨認真正應被破除的是封存規則，而非受困者。"
        )
    elif beat == "H2":
        state = (
            "【H2 唯一首次接觸／物理高潮】指定的上端厚實平整打擊端面沿 +Y 垂直向上運動，"
            "在此瞬間第一次且只第一次接觸球膜精確底點 P（6 點鐘），端面法線與接觸法線反向共線；"
            "端面與局部球膜的接觸區清楚可見。接觸以前球殼一直完整無裂，所有第一道裂紋只在接觸發生之後"
            f"從 P 放射起始，沿球面向外擴散。破裂樣式為：{fracture}。"
            "錘頭不穿進球內，錘柄與球殼保持空隙，任何側面錘頭都沒有先接觸。"
            "衝擊被局限在封存球膜；球內居民仍完整、無傷，光粒避開人體。"
            f"詩眼反轉：『{sin['promise']}』被反證；真正要打破的是機制，不是人。α={alpha} 在接觸點被回收。"
        )
    elif beat == "H3":
        state = (
            "【H3 終點錨點：球殼已解體，生命完整】沿球面傳播的裂紋全部可追溯至原底點 P；"
            f"球膜按指定樣式解體：{fracture}。殘片、光帶與折射沿遠離居民的方向溢散，沒有爆炸衝擊波，"
            "沒有碎片穿過人體，泡內承載面與居民均未被摧毀。"
            "戰錘仍保持完整剛體；指定打擊端面停在原 P 的接觸位置附近，四頭結構不變，桿身和其他錘頭不觸碰殘片或居民。"
            f"居民已全部存活、沒有傷口；{after}。他們可以選擇離開、留下、哀悼、追問或拒絕原諒，"
            "任何選擇都不由 Boundary Walker 強迫。段內 α 已被回收；下一個故事伏筆 β="
            f"{beta} 只在遠景邊緣出現，不能遮蓋生還者或改變本次接觸幾何。"
        )
    else:
        raise ValueError(f"unknown beat: {beat}")
    return base + state + "無文字、無標籤、無水印；材質與光效服務因果可讀性，不得覆蓋幾何。"


def _storyboard_9(selected: Dict[str, Tuple[str, str]], alpha: str, beta: str, mode: str) -> List[Dict[str, str]]:
    sin = selected["sin"][1]
    shell = selected["shell"][1]
    fracture = selected["fracture"][1]
    after = selected["afterglow"][1]
    descriptions = [
        f"症狀：{sin['evidence']}；球膜完整，先見異常不見破裂。",
        f"側面追蹤：{shell}的折射暴露出被隱藏的規則。",
        f"代價顯影：{sin['cost']}；居民仍活著但缺少自主性。",
        f"植入 α：{alpha}，作為第七格可回收的具體視覺物。",
        f"破局：Boundary Walker 看清真正問題是「{sin['name']}」的系統機制。",
        f"逆轉詩眼：將「{sin['promise']}」翻轉成對該承諾的質疑；球殼仍完整。",
        f"物理高潮：厚端面首次接觸球底 P，裂紋從 P 起始；{fracture}。",
        f"解放：{after}；居民生還並重新獲得選擇權。",
        f"跨故事 β：{beta}只在畫面邊緣預告另一個故事，形成可接續但不複製的伏筆。",
    ]
    cells = []
    for i, ((num, phase, operator, angle, role), description) in enumerate(zip(PHASES, descriptions), start=1):
        cells.append({
            "cell": i, "phase": phase, "operator": operator, "angle": angle,
            "narrative_role": role,
            "prompt": (
                f"3×3故事板第{i:02d}格，16:9電影單幀概念。{description} "
                f"環境為{selected['environment'][1]}；色彩為{selected['palette'][1]}。"
                f"角色模式：{_mode_anchor(mode)}"
                + (GEOMETRY_LOCK if i in (1, 4, 6, 7, 8, 9) else "")
            )
        })
    return cells


def _audit_prompts(prompts: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    errors: List[str] = []
    required = ["6 點鐘位置", "指定打擊端面", "桿身", "居民", "球膜"]
    for mode, beats in prompts.items():
        for beat in ("H0", "H1", "H2", "H3"):
            value = beats.get(beat, "")
            for token in required:
                if token not in value:
                    errors.append(f"{mode}.{beat}: missing {token}")
        if "空隙" not in beats["H0"] or "無預存裂紋" not in beats["H0"]:
            errors.append(f"{mode}.H0: start state must be intact with visible gap")
        if "第一次" not in beats["H2"] or "從 P" not in beats["H2"]:
            errors.append(f"{mode}.H2: contact and fracture origin must be explicit")
        if "全部存活" not in beats["H3"] or "沒有傷口" not in beats["H3"]:
            errors.append(f"{mode}.H3: survival invariant missing")
        if "同一攝影機位置" not in beats["H0"] or "同一攝影機位置" not in beats["H3"]:
            errors.append(f"{mode}: start/end camera lock missing")
    return {
        "status": "PROMPT_CONTRACT_PASS" if not errors else "BLOCK",
        "errors": errors,
        "image_realization": "NOT_RUN",
        "note": "This audit checks prompt text and schema only; it does not verify pixels, collision geometry, image-model adherence, or video interpolation."
    }


def build_record(index: int, mode: str = "heroine") -> Dict[str, Any]:
    if mode not in ("heroine", "abstract", "dual"):
        raise ValueError("mode must be heroine, abstract, or dual")
    digits = _decode_index(index)
    if not _is_compatible(digits):
        raise ValueError("incompatible shell/fracture pair; use an index from iter_diverse_indices")
    selected = _select_by_index(index)
    alpha, beta = _alpha_beta(index)
    camera_line = f"固定鏡位：{selected['camera'][1]}。此鏡位在 H0、H1、H2、H3 四張圖中鎖死不變。"
    modes = ("heroine", "abstract") if mode == "dual" else (mode,)
    prompts: Dict[str, Dict[str, str]] = {}
    for selected_mode in modes:
        prompts[selected_mode] = {
            beat: _prompt_for_beat(beat, selected, selected_mode, alpha, beta, camera_line)
            for beat in ("H0", "H1", "H2", "H3")
        }
    primary = prompts[modes[0]]
    sin = selected["sin"][1]
    story_id = _stable_id(selected)
    record: Dict[str, Any] = {
        "engine_version": ENGINE_VERSION,
        "story_id": story_id,
        "combination_index": index,
        "title": f"{sin['name']}｜{selected['shell'][0]}｜{selected['environment'][0]}",
        "mode": mode,
        "root_sin": sin["name"],
        "root_mechanism": sin["mechanism"],
        "human_cost": sin["cost"],
        "agency_restored": sin["choice"],
        "source_inspirations": [
            {"family":"EFV V6.4 semantic inspiration", "motif": alpha if index % 2 == 0 else beta},
            {"family":"Gumen Rock V7.0 semantic inspiration", "motif": beta if index % 2 == 0 else alpha},
        ],
        "axes": {key: {"id": pair[0], "description": pair[1]} for key, pair in selected.items()},
        "foreshadowing": {"alpha_intra_story": alpha, "beta_cross_story": beta},
        "coordinate_contract": {
            "world_up": "+Y",
            "sphere_center": "C=(0,R,0)",
            "bottom_contact": "P=C+(0,-R,0)=(0,0,0), 6 o'clock",
            "target_outward_normal": "(0,-1,0)",
            "hammer_face_normal": "(0,+1,0)=-n_target",
            "hammer_velocity": "(0,+V,0), V>0",
            "first_contact": "the thick upper terminal striking face only",
        },
        "prompts": prompts,
        "start_prompt": primary["H0"],
        "reveal_prompt": primary["H1"],
        "contact_prompt": primary["H2"],
        "end_prompt": primary["H3"],
        "negative_prompt": NEGATIVE_PROMPT,
        "storyboard_9": _storyboard_9(selected, alpha, beta, modes[0]),
        "audit": None,
    }
    record["audit"] = _audit_prompts(prompts)
    return record


def _write_json_array(path: Path, records: Iterable[Dict[str, Any]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as file:
        file.write("[\n")
        for record in records:
            if count:
                file.write(",\n")
            json.dump(record, file, ensure_ascii=False, indent=2)
            count += 1
        file.write("\n]\n")
    return count


def _write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    return count


def _write_csv(path: Path, records: Iterable[Dict[str, Any]]) -> int:
    fields = [
        "story_id","title","mode","root_sin","root_mechanism","human_cost","agency_restored",
        "start_prompt","reveal_prompt","contact_prompt","end_prompt","negative_prompt",
        "prompt_variants_json","storyboard_9_json","audit_status","audit_errors_json","image_realization"
    ]
    count = 0
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            writer.writerow({
                "story_id":r["story_id"],"title":r["title"],"mode":r["mode"],
                "root_sin":r["root_sin"],"root_mechanism":r["root_mechanism"],
                "human_cost":r["human_cost"],"agency_restored":r["agency_restored"],
                "start_prompt":r["start_prompt"],"reveal_prompt":r["reveal_prompt"],
                "contact_prompt":r["contact_prompt"],"end_prompt":r["end_prompt"],
                "negative_prompt":r["negative_prompt"],
                "prompt_variants_json":json.dumps(r["prompts"],ensure_ascii=False),
                "storyboard_9_json":json.dumps(r["storyboard_9"],ensure_ascii=False),
                "audit_status":r["audit"]["status"],
                "audit_errors_json":json.dumps(r["audit"]["errors"],ensure_ascii=False),
                "image_realization":r["audit"]["image_realization"],
            })
            count += 1
    return count


def _write_markdown(path: Path, records: Iterable[Dict[str, Any]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as file:
        file.write("# Original Sin / Wushuang Bubble-Break Prompt Batch\n\n")
        file.write("> Prompt-contract audit is not image validation. All image results remain NOT_RUN until rendered and inspected.\n\n")
        for r in records:
            count += 1
            file.write(f"## {r['story_id']} — {r['title']}\n\n")
            file.write(f"- Root sin: {r['root_sin']}\n- Mechanism: {r['root_mechanism']}\n")
            file.write(f"- Human cost: {r['human_cost']}\n- Restored agency: {r['agency_restored']}\n")
            file.write(f"- Prompt audit: {r['audit']['status']} / Image realization: {r['audit']['image_realization']}\n\n")
            file.write("### H0 — Start frame: intact membrane\n\n" + r["start_prompt"] + "\n\n")
            file.write("### H1 — Reveal the mechanism\n\n" + r["reveal_prompt"] + "\n\n")
            file.write("### H2 — First contact\n\n" + r["contact_prompt"] + "\n\n")
            file.write("### H3 — End frame: shell broken, residents safe\n\n" + r["end_prompt"] + "\n\n")
            file.write("### Negative prompt\n\n" + r["negative_prompt"] + "\n\n---\n\n")
    return count


def generate(count: int, seed: int, mode: str, fmt: str, output: str) -> Dict[str, Any]:
    if count < 1:
        raise ValueError("--count must be >= 1")
    if count > 250_000:
        raise ValueError("--count is capped at 250000 per run to keep exports predictable; use multiple seeds for larger libraries")
    if count > TOTAL_COMBINATIONS:
        raise ValueError(f"only {TOTAL_COMBINATIONS} combinations exist")
    records = (build_record(index, mode) for index in iter_diverse_indices(count, seed))
    if output == "-":
        if fmt == "jsonl":
            written = 0
            for record in records:
                print(json.dumps(record, ensure_ascii=False))
                written += 1
        else:
            print("[")
            written = 0
            for record in records:
                if written:
                    print(",")
                print(json.dumps(record, ensure_ascii=False, indent=2))
                written += 1
            print("]")
    else:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        if fmt == "json":
            written = _write_json_array(path, records)
        elif fmt == "jsonl":
            written = _write_jsonl(path, records)
        elif fmt == "csv":
            written = _write_csv(path, records)
        elif fmt == "md":
            written = _write_markdown(path, records)
        else:
            raise ValueError(f"unsupported format: {fmt}")
    return {
        "engine_version":ENGINE_VERSION,"seed":seed,"requested_count":count,
        "written_count":written,"format":fmt,"output":output,
        "combination_space":TOTAL_COMBINATIONS,"mode":mode,
        "text_contract_status":"PROMPT_CONTRACT_PASS checks required prompt text only",
        "image_realization":"NOT_RUN",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate high-diversity Original Sin / Wushuang Bubble-Break story image prompts.")
    parser.add_argument("--count",type=int,default=12,help="unique story concepts to generate (maximum 250000 per run)")
    parser.add_argument("--seed",type=int,default=20261020,help="deterministic seed")
    parser.add_argument("--mode",choices=("heroine","abstract","dual"),default="heroine",help="heroine ON, abstract foreground, or export both variants")
    parser.add_argument("--format",choices=("json","jsonl","csv","md"),default="jsonl",help="stream-friendly output format")
    parser.add_argument("--out",default="out/original_sin_bubble_break.jsonl",help="output path; use - for stdout (json/jsonl only)")
    args = parser.parse_args(argv)
    if args.out == "-" and args.format not in ("json","jsonl"):
        parser.error("--out - supports only json or jsonl")
    try:
        summary = generate(args.count,args.seed,args.mode,args.format,args.out)
    except (ValueError,OSError) as exc:
        print(f"BLOCK: {exc}",file=sys.stderr)
        return 2
    print(json.dumps(summary,ensure_ascii=False,indent=2),file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
