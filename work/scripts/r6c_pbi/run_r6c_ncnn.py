#!/usr/bin/env python3
"""R6c · option ③ NCNN accelerate GENERAL_x4v3
- convert already done via pnnx
- bench NCNN vs PyTorch vs ORT
- FULL-RES 4x residual on P0/P1 with NCNN + PBI luma-only residual DEFAULT
- optional re-VM paste if faster
"""
from __future__ import annotations
import gc, json, time, shutil
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
import ncnn

SRC = Path("/workspace/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394/MOTHER_SRC.jpg")
PTH = Path("/workspace/artifacts/artifacts/sr_contest/realesr-general-x4v3.pth")
PARAM = Path("/workspace/artifacts/artifacts/sr_contest/general_x4v3.ncnn.param")
BIN = Path("/workspace/artifacts/artifacts/sr_contest/general_x4v3.ncnn.bin")
ONNX = Path("/workspace/artifacts/artifacts/sr_contest/realesr_general_x4v3.onnx")
OUT = Path("/workspace/artifacts/SETS/PROJ_R5_SILVER_ARMOR_2394/r6c")
COMP = OUT / "complete"
for d in (OUT/"bench", OUT/"child", COMP):
    d.mkdir(parents=True, exist_ok=True)

TILE, S, GAIN, TILE_N = 64, 4, 1.10, 24
# PBI default: PREVENT BLUE INJECTION — luma-only residual · lock LP chroma
# modes: "luma_only" (default) | "legacy_rgb" (poison) | "chroma_guard"
PBI_MODE = "luma_only"  # "luma_only" | "legacy_rgb"
# GitHub path (this branch): work/scripts/r6c_pbi/run_r6c_ncnn.py
REPO_SCRIPT = "work/scripts/r6c_pbi/run_r6c_ncnn.py"
PBI_DOC = "hyb = C(LP)×(Y_LP + ridge(dY)); multi_sigma on Y only; no RGB chroma residual"

def to_y_bgr(bgr):
    f = bgr.astype(np.float32)
    return 0.114 * f[..., 0] + 0.587 * f[..., 1] + 0.299 * f[..., 2]

def chrom_bgr(bgr, y=None, y_floor: float = 8.0):
    """LP chroma; floor Y to avoid near-black blow-up (G8 risk)."""
    f = bgr.astype(np.float32)
    if y is None:
        y = to_y_bgr(f)
    y_safe = np.maximum(y, y_floor)
    return f / y_safe[..., None]


# --- G7 NEW BLUE BLOTCH / G8 NEW BLACK BLOTCH ---
def blue_opp_bgr(bgr: np.ndarray) -> np.ndarray:
    f = bgr.astype(np.float32)
    return f[..., 0] - 0.5 * (f[..., 1] + f[..., 2])


def connected_blotch(mask: np.ndarray) -> dict:
    m = (mask.astype(np.uint8) * 255)
    n, _lab, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    if n <= 1:
        return {"n": 0, "max_area": 0, "total_area": 0}
    areas = stats[1:, cv2.CC_STAT_AREA]
    return {"n": int(len(areas)), "max_area": int(areas.max()), "total_area": int(areas.sum())}


def gate_g7_new_blue(lp_bgr: np.ndarray, out_bgr: np.ndarray,
                     y_lo: float = 25.0, y_hi: float = 200.0,
                     d_thr: float = 8.0, total_area_max: int = 8000) -> dict:
    """Compare LP vs OUT: new blue opponent excess on Y-valid pixels."""
    y = to_y_bgr(lp_bgr)
    valid = (y >= y_lo) & (y <= y_hi)
    d = blue_opp_bgr(out_bgr) - blue_opp_bgr(lp_bgr)
    new_blue = (d > d_thr) & valid
    bl = connected_blotch(new_blue)
    mean_abs = float(np.abs(d)[valid].mean()) if valid.any() else 0.0
    out = {
        "mean_abs_blue_delta": round(mean_abs, 4),
        "new_blue_px": int(new_blue.sum()),
        "blotch_n": bl["n"],
        "blotch_max_area": bl["max_area"],
        "blotch_total_area": bl["total_area"],
        "PASS": bl["total_area"] <= total_area_max and bl["max_area"] <= max(2000, total_area_max // 2),
    }
    return out


def gate_g8_new_black(lp_bgr: np.ndarray, out_bgr: np.ndarray,
                      black_thr: float = 18.0,
                      total_area_max: int = 6000, max_area_max: int = 900) -> dict:
    """New near-black vs LP: catch over-negative Y residual collapse."""
    y_lp = to_y_bgr(lp_bgr)
    y_out = to_y_bgr(out_bgr)
    black_lp = y_lp < black_thr
    black_out = y_out < black_thr
    new_black = black_out & (~black_lp)
    bl = connected_blotch(new_black)
    # wire damage proxy: new black on high-edge LP
    g = cv2.cvtColor(lp_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    mag = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0, 3), cv2.Sobel(g, cv2.CV_32F, 0, 1, 3))
    wire = mag > (mag.mean() + 0.5 * mag.std())
    wire_hit = int((new_black & wire).sum())
    out = {
        "new_black_px": int(new_black.sum()),
        "blotch_n": bl["n"],
        "blotch_max_area": bl["max_area"],
        "blotch_total_area": bl["total_area"],
        "wire_hit_px": wire_hit,
        "PASS": bl["total_area"] <= total_area_max and bl["max_area"] <= max_area_max and wire_hit < 1500,
    }
    return out


def write_sha256sums(paths, out_txt: Path, note_manifest: Path | None = None) -> dict:
    import hashlib
    entries = []
    lines = []
    for p in paths:
        p = Path(p)
        if not p.is_file():
            continue
        b = p.read_bytes()
        h = hashlib.sha256(b).hexdigest()
        rel = str(p)
        entries.append({"path": rel, "sha256": h, "bytes": len(b)})
        lines.append(f"{h}  {rel}")
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    out_txt.write_text("\n".join(lines) + "\n")
    sh = __import__("hashlib").sha256(out_txt.read_bytes()).hexdigest()
    man = {
        "asof": datetime.now(timezone.utc).isoformat(),
        "rule": "entries exclude MANIFEST self-hash; verify with this SHA256SUMS sidecar",
        "sha256sums_sidecar": {"path": str(out_txt), "sha256": sh, "bytes": out_txt.stat().st_size},
        "entries": entries,
    }
    if note_manifest is not None:
        note_manifest.write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n")
        # separate note for manifest file hash
        mh = __import__("hashlib").sha256(note_manifest.read_bytes()).hexdigest()
        (out_txt.parent / "SHA256_MANIFEST_NOTE.txt").write_text(
            f"{mh}  {note_manifest}\n{sh}  {out_txt}\n"
        )
    return man

def multi_sigma_fill_y(res_y, weight, sigmas=(4, 8, 16)):
    """Fill only on Y residual — do not spread chroma (E-BLUE-02)."""
    filled = np.zeros_like(res_y, dtype=np.float32)
    wacc = np.zeros(weight.shape, np.float32)
    for s in sigmas:
        filled += cv2.GaussianBlur(res_y, (0, 0), s)
        wacc += cv2.GaussianBlur(weight, (0, 0), s)
    filled /= np.maximum(wacc, 1e-6)
    m = (weight > 0.15).astype(np.float32)
    return res_y * m + filled * (1.0 - m)

def ridge_hard_y(residual_y, parent_hd, thr_k=0.35, dil=3):
    g = cv2.cvtColor(parent_hd, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    mag = cv2.magnitude(gx, gy)
    thr = float(mag.mean() + thr_k * mag.std())
    hard = (mag > thr).astype(np.uint8)
    hard = cv2.dilate(hard, np.ones((2 * dil + 1, 2 * dil + 1), np.uint8), 1)
    inv = (1 - hard).astype(np.uint8)
    dist = cv2.distanceTransform(inv, cv2.DIST_L2, 3)
    soft = np.maximum(hard.astype(np.float32), np.exp(-(dist ** 2) / (2 * 2.2 ** 2)) * (1 - hard))
    soft = np.clip(cv2.GaussianBlur(soft, (0, 0), 1.2), 0, 1)
    cell = (mag < mag.mean() * 0.55).astype(np.float32)
    cell = cv2.erode(cell, np.ones((3, 3), np.uint8), 1)
    gate = np.clip(soft * (1 - 0.85 * cell * (1 - soft)), 0, 1)
    gate_p = np.power(gate, 0.65)
    res_h = residual_y * gate_p * (1.0 + 0.25 * hard.astype(np.float32))
    rmag = np.abs(res_h)
    align = float((rmag * soft).sum() / (rmag.sum() + 1e-8))
    spill = float((rmag * (1 - soft)).sum() / (rmag.sum() + 1e-8))
    return res_h, align, spill

def pbi_compose_from_rgb_residual(LP_bgr, residual_rgb, parent_hd, mode=None):
    """Compose hybrid with PBI default.
    residual_rgb is BGR residual (SR-LP) after optional fill/mask/gain.
    """
    mode = mode or PBI_MODE
    if mode == "legacy_rgb":
        res_h, align, spill = ridge_hard(residual_rgb, parent_hd, 0.35, 3)
        hyb = np.clip(LP_bgr + res_h, 0, 255).astype(np.uint8)
        return hyb, align, spill, mode
    # luma-only / chroma_guard share: ridge on dY then lock LP chrom
    dy = to_y_bgr(residual_rgb)  # residual channels already BGR deltas
    # if residual is full RGB, Y of residual ≈ dY
    res_y, align, spill = ridge_hard_y(dy, parent_hd, 0.35, 3)
    y_lp = to_y_bgr(LP_bgr)
    y_out = y_lp + res_y
    hyb = np.clip(chrom_bgr(LP_bgr, y_lp) * y_out[..., None], 0, 255).astype(np.uint8)
    return hyb, align, spill, mode

class SRVGG(nn.Module):
    def __init__(self, nf=64, nc=32, s=4):
        super().__init__()
        self.upscale=s
        self.body=nn.ModuleList()
        self.body.append(nn.Conv2d(3,nf,3,1,1)); self.body.append(nn.PReLU(nf))
        for _ in range(nc):
            self.body.append(nn.Conv2d(nf,nf,3,1,1)); self.body.append(nn.PReLU(nf))
        self.body.append(nn.Conv2d(nf,3*(s**2),3,1,1))
        self.upsampler=nn.PixelShuffle(s)
    def forward(self,x):
        out=x
        for m in self.body: out=m(out)
        out=self.upsampler(out)
        return out+F.interpolate(x, scale_factor=self.upscale, mode='nearest')

def load_pt():
    m=SRVGG()
    ck=torch.load(str(PTH), map_location='cpu')
    if isinstance(ck,dict):
        for k in ('params_ema','params','state_dict','model'):
            if k in ck and isinstance(ck[k], dict):
                ck=ck[k]; break
    m.load_state_dict({(k[7:] if k.startswith('module.') else k):v for k,v in ck.items()}, strict=True)
    m.eval(); return m

def load_ncnn(threads=2):
    net=ncnn.Net()
    net.opt.use_vulkan_compute=False
    net.opt.num_threads=threads
    net.load_param(str(PARAM))
    net.load_model(str(BIN))
    return net

@torch.no_grad()
def pt_4x(model, bgr):
    rgb=cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32)/255.0
    t=torch.from_numpy(np.ascontiguousarray(rgb.transpose(2,0,1)[None]))
    o=model(t).clamp(0,1).numpy()[0].transpose(1,2,0)
    return cv2.cvtColor((o*255).round().astype(np.uint8), cv2.COLOR_RGB2BGR)

def ncnn_4x(net, bgr):
    h,w=bgr.shape[:2]
    # E-R6C-01: do NOT use PIXEL_BGR2RGB on BGR buffer (double-swap poison).
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    mat_in=ncnn.Mat.from_pixels(rgb, ncnn.Mat.PixelType.PIXEL_RGB, w, h)
    mat_in.substract_mean_normalize([0,0,0],[1/255.,1/255.,1/255.])
    ex=net.create_extractor()
    assert ex.input('in0', mat_in)==0
    ret, mat_out = ex.extract('out0')
    assert ret==0, ret
    # CHW float
    arr=np.array(mat_out)
    if arr.ndim==1:
        arr=arr.reshape(3, h*4, w*4)
    elif arr.ndim==3 and arr.shape[0]==3:
        pass
    else:
        # sometimes HWC
        if arr.shape[-1]==3:
            arr=arr.transpose(2,0,1)
        else:
            arr=arr.reshape(3, h*4, w*4)
    out=np.clip(arr.transpose(1,2,0)*255,0,255).round().astype(np.uint8)
    return cv2.cvtColor(out, cv2.COLOR_RGB2BGR)

def tenengrad(img):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx=cv2.Sobel(g,cv2.CV_32F,1,0,3); gy=cv2.Sobel(g,cv2.CV_32F,0,1,3)
    return float((gx*gx+gy*gy).mean())

def struct_ncc(a,b):
    ga=cv2.GaussianBlur(cv2.cvtColor(a,cv2.COLOR_BGR2GRAY).astype(np.float32),(0,0),2)
    gb=cv2.GaussianBlur(cv2.cvtColor(b,cv2.COLOR_BGR2GRAY).astype(np.float32),(0,0),2)
    ga=cv2.resize(ga,(max(1,ga.shape[1]//2),max(1,ga.shape[0]//2)),interpolation=cv2.INTER_AREA)
    gb=cv2.resize(gb,(ga.shape[1],ga.shape[0]),interpolation=cv2.INTER_AREA)
    aa,bb=ga-ga.mean(), gb-gb.mean()
    return float((aa*bb).sum()/((np.linalg.norm(aa)*np.linalg.norm(bb))+1e-8))

def pick_peeps(bgr, size=512, n=2):
    hsv=cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    lab=cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    silver=cv2.inRange(hsv,(0,0,55),(180,70,255))
    gold=cv2.inRange(hsv,(10,40,60),(40,255,255))
    L=lab[:,:,0]; mid=((L>45)&(L<220)).astype(np.uint8)*255
    mask=cv2.bitwise_and(cv2.bitwise_or(silver,gold), mid)
    h,w=bgr.shape[:2]
    g=cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx=cv2.Sobel(g,cv2.CV_32F,1,0,3); gy=cv2.Sobel(g,cv2.CV_32F,0,1,3)
    mag=cv2.magnitude(gx,gy)*(mask.astype(np.float32)/255.0)
    k=np.ones((size,size),np.float32)/(size*size)
    energy=cv2.filter2D(mag,-1,k)
    dens=cv2.filter2D(mask.astype(np.float32)/255.0,-1,k)
    score=energy*(0.35+0.65*dens)
    peeps=[]; sw=score.copy()
    for _ in range(n):
        margin=size//2+4
        s=sw.copy(); s[:margin]=0; s[-margin:]=0; s[:,:margin]=0; s[:,-margin:]=0
        s[dens<0.18]=0
        y,x=np.unravel_index(np.argmax(s), s.shape)
        y0=max(0,min(h-size,int(y)-size//2)); x0=max(0,min(w-size,int(x)-size//2))
        peeps.append((x0,y0,size,size))
        sw[max(0,y-size):min(h,y+size), max(0,x-size):min(w,x+size)]*=0.05
    return peeps

def pick_probes(L0, tile=64, target=24, min_step=32):
    g=cv2.cvtColor(L0,cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx=cv2.Sobel(g,cv2.CV_32F,1,0,3); gy=cv2.Sobel(g,cv2.CV_32F,0,1,3)
    mag=cv2.magnitude(gx,gy)
    k=np.ones((tile,tile),np.float32)/(tile*tile)
    energy=cv2.filter2D(mag,-1,k)
    h,w=g.shape; cands=[]
    for y in range(0,h-tile+1,min_step):
        for x in range(0,w-tile+1,min_step):
            cands.append((float(energy[y+tile//2,x+tile//2]),y,x))
    cands.sort(reverse=True)
    chosen=[]; occ=np.zeros((h,w),np.float32)
    for e,y,x in cands:
        if len(chosen)>=target: break
        if float(occ[y:y+tile,x:x+tile].mean())<0.35:
            chosen.append((y,x)); occ[y:y+tile,x:x+tile]+=1
    return chosen

def multi_sigma_fill(res, weight, sigmas=(4,8,16)):
    filled=np.zeros_like(res); wacc=np.zeros(weight.shape, np.float32)
    for s in sigmas:
        for c in range(3):
            filled[:,:,c]+=cv2.GaussianBlur(res[:,:,c],(0,0),s)
        wacc+=cv2.GaussianBlur(weight,(0,0),s)
    filled/=np.maximum(wacc[:,:,None],1e-6)
    m=(weight>0.15).astype(np.float32)[:,:,None]
    return res*m+filled*(1-m)

def ridge_hard(residual, parent_hd, thr_k=0.35, dil=3):
    g=cv2.cvtColor(parent_hd,cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx=cv2.Sobel(g,cv2.CV_32F,1,0,3); gy=cv2.Sobel(g,cv2.CV_32F,0,1,3)
    mag=cv2.magnitude(gx,gy)
    thr=float(mag.mean()+thr_k*mag.std())
    hard=(mag>thr).astype(np.uint8)
    hard=cv2.dilate(hard,np.ones((2*dil+1,2*dil+1),np.uint8),1)
    inv=(1-hard).astype(np.uint8)
    dist=cv2.distanceTransform(inv,cv2.DIST_L2,3)
    soft=np.maximum(hard.astype(np.float32), np.exp(-(dist**2)/(2*2.2**2))*(1-hard))
    soft=np.clip(cv2.GaussianBlur(soft,(0,0),1.2),0,1)
    cell=(mag<mag.mean()*0.55).astype(np.float32)
    cell=cv2.erode(cell,np.ones((3,3),np.uint8),1)
    gate=np.clip(soft*(1-0.85*cell*(1-soft)),0,1)
    gate_p=np.power(gate,0.65)
    res_h=residual*gate_p[:,:,None]*(1.0+0.25*hard.astype(np.float32))[:,:,None]
    rmag=np.linalg.norm(res_h,axis=2)
    align=float((rmag*soft).sum()/(rmag.sum()+1e-8))
    spill=float((rmag*(1-soft)).sum()/(rmag.sum()+1e-8))
    return res_h, align, spill

def bench(full):
    crop=full[693:693+64, 300:300+64].copy()
    pt=load_pt(); net=load_ncnn(2)
    # fidelity
    a=pt_4x(pt, crop); b=ncnn_4x(net, crop)
    mae=float(np.mean(np.abs(a.astype(np.float32)-b.astype(np.float32))))
    ncc=struct_ncc(a,b)
    # speed
    for fn,name in [(lambda: pt_4x(pt,crop),'PT'), (lambda: ncnn_4x(net,crop),'NCNN')]:
        for _ in range(5): fn()
    times={}
    for fn,name,n in [(lambda: pt_4x(pt,crop),'PT',30), (lambda: ncnn_4x(net,crop),'NCNN',30)]:
        t0=time.time()
        for _ in range(n): fn()
        times[name]=(time.time()-t0)/n*1000
    # ORT if exists
    if ONNX.exists():
        import onnxruntime as ort
        sess=ort.InferenceSession(str(ONNX), providers=['CPUExecutionProvider'])
        def ort_4x(bgr):
            rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB).astype(np.float32)/255.0
            x=rgb.transpose(2,0,1)[None]
            y=sess.run(None,{'input':x})[0][0].transpose(1,2,0)
            return cv2.cvtColor(np.clip(y*255,0,255).round().astype(np.uint8), cv2.COLOR_RGB2BGR)
        for _ in range(5): ort_4x(crop)
        t0=time.time()
        for _ in range(30): ort_4x(crop)
        times['ORT']=(time.time()-t0)/30*1000
        c=ort_4x(crop)
        times['ORT_mae_vs_PT']=float(np.mean(np.abs(a.astype(np.float32)-c.astype(np.float32))))
    res=dict(mae_ncnn_vs_pt=mae, ncc_ncnn_vs_pt=ncc, ms=times,
             speedup_vs_pt={k: round(times['PT']/v,2) for k,v in times.items() if k in ('NCNN','ORT') and isinstance(v,(int,float))},
             note='Vulkan binary unavailable (libvulkan missing + noexec) · used pyncnn CPU from pnnx convert')
    (OUT/'bench'/'BENCH_NCNN.json').write_text(json.dumps(res, indent=2))
    print('BENCH', json.dumps(res, indent=2), flush=True)
    # save compare strip
    panels=[]
    for im,t in [(crop,'L0 64'),(a,'PT 256'),(b,'NCNN 256')]:
        p=cv2.resize(im,(160,160) if im.shape[0]==64 else (160,160), interpolation=cv2.INTER_NEAREST if im.shape[0]==64 else cv2.INTER_AREA)
        c=np.zeros((180,160,3),np.uint8); c[20:]=p
        cv2.putText(c,t,(4,14),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,180),1,cv2.LINE_AA)
        panels.append(c)
    strip=np.hstack(panels)
    cv2.imwrite(str(OUT/'bench'/'COMPARE_PT_NCNN.jpg'), strip, [int(cv2.IMWRITE_JPEG_QUALITY),92])
    return res, pt, net

def spm_fullres_ncnn(net, L0, n_probes=24):
    assert L0.shape[0]==512
    Hh=Wh=512*S
    LP=cv2.resize(L0,(Wh,Hh),interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    probes=pick_probes(L0, TILE, n_probes, 32)
    print(f'  NCNN fullres probes {len(probes)}', flush=True)
    res_acc=np.zeros((Hh,Wh,3),np.float32)
    res_y_acc=np.zeros((Hh,Wh),np.float32)
    w_acc=np.zeros((Hh,Wh),np.float32)
    yy,xx=np.mgrid[0:TILE,0:TILE]; c=(TILE-1)/2.0
    gw=np.exp(-((yy-c)**2+(xx-c)**2)/(2*(TILE*0.28)**2)).astype(np.float32)
    t0=time.time()
    for i,(y,x) in enumerate(probes):
        tile=L0[y:y+TILE,x:x+TILE]
        sr4=ncnn_4x(net, tile).astype(np.float32)
        lp4=cv2.resize(tile,(256,256),interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
        # accumulate dY (luma residual) + optional RGB for legacy
        dy = to_y_bgr(sr4) - to_y_bgr(lp4)
        r = sr4 - lp4  # kept for legacy_rgb only
        Y,X=y*S,x*S
        th,tw=r.shape[:2]
        ww=cv2.resize(gw,(tw,th),interpolation=cv2.INTER_LINEAR)
        res_acc[Y:Y+th,X:X+tw]+=r*ww[:,:,None]
        res_y_acc[Y:Y+th,X:X+tw]+=dy*ww
        w_acc[Y:Y+th,X:X+tw]+=ww
        if (i+1)%8==0:
            print(f'    {i+1}/{len(probes)}', flush=True)
    infer_s=time.time()-t0
    parent_hd=cv2.resize(L0,(Wh,Hh),interpolation=cv2.INTER_LANCZOS4)
    if PBI_MODE == "legacy_rgb":
        res=res_acc/np.maximum(w_acc[:,:,None],1e-6)
        filled=multi_sigma_fill(res, w_acc)
        mag=np.linalg.norm(filled,axis=2)
        rough=(mag>(mag.mean()+0.5*mag.std())).astype(np.float32)
        M=np.clip(w_acc/(w_acc.max()+1e-6),0,1)
        M=np.clip(M+0.85*rough*0.5,0,1)
        residual_new=filled*M[:,:,None]*GAIN
        hyb, align, spill, mode = pbi_compose_from_rgb_residual(LP, residual_new, parent_hd, "legacy_rgb")
    else:
        # PBI default: multi_sigma on Y only (E-BLUE-02 kill) + ridge Y + lock LP chrom
        res_y = res_y_acc / np.maximum(w_acc, 1e-6)
        filled_y = multi_sigma_fill_y(res_y, w_acc)
        mag = np.abs(filled_y)
        rough = (mag > (mag.mean() + 0.5 * mag.std())).astype(np.float32)
        M = np.clip(w_acc / (w_acc.max() + 1e-6), 0, 1)
        M = np.clip(M + 0.85 * rough * 0.5, 0, 1)
        residual_y = filled_y * M * GAIN
        res_h_y, align, spill = ridge_hard_y(residual_y, parent_hd, 0.35, 3)
        y_lp = to_y_bgr(LP)
        y_out = y_lp + res_h_y
        # G8: do not allow new near-black collapse far below LP (keep mesh holes from LP)
        y_floor = np.maximum(y_lp - 36.0, 5.0)
        y_out = np.clip(y_out, y_floor, 255.0)
        hyb = np.clip(chrom_bgr(LP, y_lp) * y_out[..., None], 0, 255).astype(np.uint8)
        mode = PBI_MODE
    meta=dict(n_probes=len(probes), child_hw=Wh, align=align, spill=spill,
              ten=tenengrad(hyb), sn=struct_ncc(LP.astype(np.uint8), hyb),
              infer_s=round(infer_s,2), engine='NCNN_GENERAL_x4v3',
              iron='4x_MODEL_to_4x_RESIDUAL_PBI_LUMA',
              pbi_mode=mode, pbi=PBI_DOC)
    return hyb, meta

def main():
    t0=time.time()
    torch.set_num_threads(2)
    full=cv2.imread(str(SRC)); assert full is not None
    print('FULL', full.shape[1], full.shape[0], 'R6c NCNN', flush=True)
    bench_res, pt, net = bench(full)
    peeps=pick_peeps(full)
    print('peeps', peeps, flush=True)
    results=[]
    for pi,(x0,y0,pw,ph) in enumerate(peeps):
        tag=f'P{pi}'
        L0=full[y0:y0+ph,x0:x0+pw].copy()
        print(f'{tag} NCNN FULLRES…', flush=True)
        hyb, meta = spm_fullres_ncnn(net, L0, TILE_N)
        path=COMP/f'{tag}_CHILD_2048_NCNN_PBI_R6c.png'
        cv2.imwrite(str(path), hyb, [cv2.IMWRITE_PNG_COMPRESSION,3])
        print(f'  {tag} align={meta["align"]:.3f} ten={meta["ten"]:.0f} infer={meta["infer_s"]}s bytes={path.stat().st_size}', flush=True)
        # G7/G8 on full child vs Lanczos LP parent
        LP_u8 = cv2.resize(L0, (hyb.shape[1], hyb.shape[0]), interpolation=cv2.INTER_LANCZOS4)
        g7 = gate_g7_new_blue(LP_u8, hyb)
        g8 = gate_g8_new_black(LP_u8, hyb)
        struct_ok = meta['align'] >= 0.65 and meta['sn'] >= 0.97
        pass_all = struct_ok and g7['PASS'] and g8['PASS']
        results.append(dict(
            tag=tag, xy=[x0, y0], meta=meta, child=str(path), bytes=path.stat().st_size,
            G7_blue=g7, G8_black=g8,
            PASS_struct=struct_ok, PASS=pass_all,
        ))
        # strip LP | OUT
        lp=cv2.resize(L0,(256,256),interpolation=cv2.INTER_AREA)
        ch=cv2.resize(hyb,(256,256),interpolation=cv2.INTER_AREA)
        strip=np.hstack([lp,ch])
        cv2.imwrite(str(COMP/f'{tag}_PROOF.jpg'), strip, [int(cv2.IMWRITE_JPEG_QUALITY),90])
        # diff overlay preview
        dlt = np.abs(ch.astype(np.float32) - lp.astype(np.float32))
        dlt = np.clip(dlt * 3.0, 0, 255).astype(np.uint8)
        cv2.imwrite(str(COMP/f'{tag}_DIFF.jpg'), np.hstack([lp, ch, dlt]), [int(cv2.IMWRITE_JPEG_QUALITY),90])
        print(f'  {tag} G7_blue PASS={g7["PASS"]} area={g7["blotch_total_area"]} G8_black PASS={g8["PASS"]} area={g8["blotch_total_area"]}', flush=True)
        del hyb; gc.collect()

    # speed note vs R6b PT 24 probes ~54ms each = ~1.3s infer; NCNN should be similar or better
    accept = dict(
        round="R6c_NCNN_PBI_LUMA_DEFAULT",
        option=3,
        constitution="§0.12.56 + G7/G8 blotch gates",
        image_generation="THIS_RUN",
        scripts={"r6c": REPO_SCRIPT, "PBI_MODE": PBI_MODE},
        formula=PBI_DOC,
        bench=bench_res,
        peeps=results,
        n_accept=sum(1 for r in results if r["PASS"]),
        n_struct=sum(1 for r in results if r.get("PASS_struct")),
        status="ACCEPT" if results and all(r["PASS"] for r in results) else "PARTIAL",
        gates_note={
            "struct": "align>=0.65 and sn>=0.97",
            "G7": "new blue blotch vs LP (Y-valid)",
            "G8": "new black blotch + wire_hit vs LP",
            "blue_pct_89": "historical P0 ROI report only · not full-frame formal gate",
        },
        limits=[
            "realesrgan-ncnn-vulkan: libvulkan missing · pyncnn CPU",
            "global LP chroma lock · not human silver-only mask",
            "clean-checkout without /workspace models cannot rerun",
        ],
        merge_main="NO",
        asof=datetime.now(timezone.utc).isoformat(),
        elapsed_s=round(time.time() - t0, 2),
    )
    (COMP / "ACCEPT_R6c_PBI.json").write_text(json.dumps(accept, indent=2, ensure_ascii=False))
    log_path = OUT / "LOG_R6c_PBI.md"
    lines = [
        "# R6c · NCNN PBI + G7/G8",
        "",
        "- image_generation: THIS_RUN",
        f"- PBI_MODE={PBI_MODE}",
        f"- status={accept['status']} n_accept={accept['n_accept']} n_struct={accept['n_struct']}",
        "- merge_main: NO",
        f"- elapsed_s={accept['elapsed_s']}",
        "",
        "## peeps G7/G8",
    ]
    for r in results:
        lines.append(
            f"- {r['tag']}: PASS={r['PASS']} struct={r.get('PASS_struct')} "
            f"G7={r['G7_blue']['PASS']} area={r['G7_blue']['blotch_total_area']} "
            f"G8={r['G8_black']['PASS']} area={r['G8_black']['blotch_total_area']}"
        )
    log_path.write_text("\n".join(lines) + "\n")
    sha_list = [r["child"] for r in results]
    for r in results:
        for suf in ("_PROOF.jpg", "_DIFF.jpg"):
            pp = COMP / f"{r['tag']}{suf}"
            if pp.is_file():
                sha_list.append(str(pp))
    sha_list += [str(COMP / "ACCEPT_R6c_PBI.json"), str(log_path)]
    write_sha256sums(sha_list, COMP / "SHA256SUMS_PBI.txt", COMP / "MANIFEST_SHA256_R6c_PBI.json")
    print(json.dumps(accept, indent=2, ensure_ascii=False), flush=True)
    print('DONE R6c', flush=True)

if __name__=='__main__':
    main()
