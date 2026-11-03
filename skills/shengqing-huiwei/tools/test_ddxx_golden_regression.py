#!/usr/bin/env python3
"""Run the DDXX manual-panel fixture as a solver regression, not an image-quality test."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np

def fit_umeyama(X, Y, w):
    sw = float(w.sum())
    xm = np.sum(X * w[:, None], axis=0) / sw
    ym = np.sum(Y * w[:, None], axis=0) / sw
    Xc, Yc = X - xm, Y - ym
    H = (Xc * w[:, None]).T @ Yc
    U, singular, Vt = np.linalg.svd(H)
    sign = 1.0 if np.linalg.det(U @ Vt) >= 0 else -1.0
    D = np.diag([1.0, sign])
    R = U @ D @ Vt
    denom = float(np.sum(w * np.sum(Xc * Xc, axis=1)))
    scale = float(np.sum(singular * np.array([1.0, sign])) / denom)
    t = ym - scale * (xm @ R)
    pred = scale * (X @ R) + t
    residual = np.linalg.norm(pred - Y, axis=1)
    mean = float(np.average(residual, weights=w))
    rmse = float(np.sqrt(np.average(residual ** 2, weights=w)))
    theta = math.degrees(math.atan2(float(R[0, 1]), float(R[0, 0])))
    return scale, theta, t, mean, rmse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", type=Path, default=Path(__file__).resolve().parents[1] / "references" / "DDXX_MANUAL_PANEL_GOLD_01.json")
    ap.add_argument("--out", type=Path, default=Path("DDXX_GOLDEN_REGRESSION_REPORT.json"))
    args = ap.parse_args()
    fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
    rows = fixture["landmarks"]
    X = np.asarray([r["donor_xy"] for r in rows], dtype=float)
    Y = np.asarray([r["target_xy"] for r in rows], dtype=float)
    w = np.asarray([r["weight"] for r in rows], dtype=float)
    a, theta, t, mean, rmse = fit_umeyama(X, Y, w)
    exp = fixture["expected"]
    tol = fixture["tolerance"]
    checks = {
        "scale": abs(a - exp["scale_a"]) <= tol["scale_a_abs"],
        "rotation": abs(theta - exp["rotation_degrees_row_convention"]) <= tol["rotation_degrees_abs"],
        "translation_x": abs(float(t[0]) - exp["translation_target_px"][0]) <= tol["translation_px_abs"],
        "translation_y": abs(float(t[1]) - exp["translation_target_px"][1]) <= tol["translation_px_abs"],
        "weighted_rmse": abs(rmse - exp["weighted_rmse_px"]) <= tol["weighted_rmse_px_abs"]
    }
    result = {
        "fixture_id": fixture["fixture_id"],
        "purpose": "solver regression only; not pose or production image acceptance",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "actual": {"scale_a": a, "rotation_degrees_row_convention": theta,
                   "translation_target_px": [float(t[0]), float(t[1])],
                   "weighted_mean_residual_px": mean, "weighted_rmse_px": rmse}
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 2)

if __name__ == "__main__":
    main()
