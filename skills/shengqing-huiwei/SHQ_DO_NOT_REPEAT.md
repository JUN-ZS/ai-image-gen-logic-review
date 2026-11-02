# 升清回位 · 勿再犯（E-SHQ / E-SCH）
> asof 2026-11-03T06:45+08 · write 01263 · 試錯入憲
> 碼：E-SHQ-nn ≡ E-SCH-nn

| ID | 禁 | 現象 | 治 |
|----|-----|------|-----|
| E-SHQ-01 | **縮小 DONOR 遷就小風景槽** | 臉糊 · 「騙 PIXEL」 | person_scale=1.0 · 放大 Scene / VM |
| E-SHQ-02 | Imagine **全圖軟融** / 重生當「貼回」 | 身份被洗 · 非硬貼 | HARDPASTE · 只改 peep 像素 |
| E-SHQ-03 | 把 **PATH1E 臉的單 ECC** 直接套全身 | cc 崩 · 雙影 | 分區 ROI 或 ANTHRO-FIT + plate |
| E-SHQ-04 | **錨點落空**（臉在天空、肩在空氣） | 假 REJECT_POSE · 假高 residual | ANCHOR-AUDIT 同法定位 |
| E-SHQ-05 | peep **裁掉披風尾/腳** 當完整人 | cape 對不齊 | PEEP 全披風留白 · cape mask 分家 |
| E-SHQ-06 | **遠人 peep 過小**（如 96×197）硬放大當姿 | 姿不穩 | **中距優先** peep ≥25–35% 高 或 PLATE-POSE |
| E-SHQ-07 | OpenCV **大 mask+inpaint 連岩剷** | 峰頂挖空 · 人浮空 | **IMAGINE-DEL** region 只人 |
| E-SHQ-08 | YOLO/自動框 **誤抓山腳小人** 當峰頂人 | DEL 錯位 | ANTHRO 峰頂 mask / 人工圈 |
| E-SHQ-09 | 鎖小母圖尺寸 + 大 donor + 1.0 **三同時** | 數學矛盾 | VM-LOCK 擴畫布 · formal 不回縮 |
| E-SHQ-10 | 單用臉心對準就稱全身完成 | 腳浮 · 披風錯 | Face/Torso/Hands/Legs 分組殘差 |
| E-SHQ-11 | sole mask **吃玄武岩** | 腳 residual 假大 | person/rock 分 mask |
| E-SHQ-12 | **panel 拼圖尺度** 當 native 尺度 | a_panel≠a_native | 原生圖重算 a,R,t |
| E-SHQ-13 | 錯稱 soft α / PBI 混成為「憲技拼回」 | 名實不符 | 拼回=公式鎖位+HARDPASTE |
| E-SHQ-14 | 姿不合仍 **非等比例拉人** | 畸變 | REJECT_POSE · 換同姿 HD donor |
| E-SHQ-15 | 為消黑帶 **再縮人 / 全圖 blur 山** | 像素與山毀 | SOLE-SUPPORT 只補腳下 · 山保持 |
| E-SHQ-16 | Haar/眼心 **混稱同一個 face** 不記來源 | 殘差不可比 | 記 face_box_center / eye_mid / used |
| E-SHQ-17 | 未鎖位就反覆 GEN 新人物 | 槽漂 · 毒疊 | 先 COREFIT 鎖 · CLEAN-REPASTE |
| E-SHQ-18 | half / 預覽圖 **冒充原 SIZE** | 驗收騙 | formal 必 VM 原尺寸 |
| **E-SHQ-19** | **跳過 COREFIT 公式** peep 糊貼 | 非 SHQ-BEST | 先 `q=a(Rp)+t` |
| **E-SHQ-20** | HD 地平與原圖 sole **水平不一致** | 腳斜浮 | PLATE 雙腳同水平 + GROUND_LOCK |
| **E-SHQ-21** | 極遠 peep 全 inverse S **OOM 或縮人** | 失敗/騙像素 | 中距；S_cap 須標；人仍 1.0 |
| **E-SHQ-22** | 把 half 預覽當 formal | 驗收騙 | formal = VM 原尺寸 |
| **E-SHQ-23** | Legs residual **進 a 或縮人換 FULL** | 破壞 1.0 | Legs 只報告；FULL 另開 |

**口訣：** 公式先；人永遠 1.0；山可放大；刪人只圈人；地平要齊；貼回要 exact；錨錯先修錨。

## 曾用失敗方法（備註 · 不可再當完成路徑）

| 方法 | 結果 | 歸檔 |
|------|------|------|
| Imagine soft fusion 全身 | 降智換臉感 | E-SHQ-02/13 |
| donor resize 對小槽 | PIXEL 被騙 | E-SHQ-01 |
| 單 ECC 全身 hetero peep | cc~0.10 | E-SHQ-03 |
| DDXX-AR v1 錯錨拒姿 | 假 32° 軀幹差 | E-SHQ-04 |
| OpenCV dilate+Telea 大剷 | 峰毀人浮 | E-SHQ-07 |
| YOLO 山腳 person | mask 錯 | E-SHQ-08 |
| 96×197 遠 peep×17 | 姿資訊不足 | E-SHQ-06 |
| 腳 residual 反驅動縮人 | 破壞 1.0 | E-SHQ-01/10 |
| 跳過公式 peep 直接縮放貼 | 非優先法 | E-SHQ-19 |
| HD 腳線斜於岩台 | 地平錯 | E-SHQ-20 |
