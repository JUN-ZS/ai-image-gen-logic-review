# 污染記錄 · 洞不能這樣回 · 新女畫錯 LOG 進化 DNA

**用戶：** 你被污染了，記錄，洞不能這樣回；看「新女畫」的錯 LOG 去進化自 DNA。

---

## 1. 污染是什麼

| 錯做（本代理 F8_TRY / DEBUG 回） | 新女畫判定 |
|----------------------------------|------------|
| `RETURN = L0; RETURN[M] = freeframe_I[M]` | **E-XHN2-01 / E-WLF3-01** 無洞 freeframe 裁貼冒充洞回 |
| outside=0 對 base 即喊 PASS | **不足**；fill 必須 **生@洞座** 產出 |
| freeframe 全圖 生 再 kou 洞區 | **E-XHN2-03** 跳洞直貼 |
| 半身/自 peep 洞 | **E-XHN2-02** 假洞 |

> **hardpaste 是證，不是生。**  
> **洞回 = 外力生 base=L_empty 只填洞；不是 freeframe 偷像素。**

---

## 2. 新女畫錯 LOG 錨

| 案 | 錯圖 / 改正 |
|----|-------------|
| 01463 ERROR_TEXTBOOK | `E_XHN2_01_RETURN_WITHOUT_HOLE` · `SELF_PEEP_FAKE_HOLE` |
| 01463-FIX | CLIP←除背扣；洞←除頭同框；生 on L_empty；禁硬 1:1 |
| 01436 woman | Q6 no freeframe steal；除 local 優於 global |
| 01464 定稿 | 生只在洞座 · 無洞回/自peep = ERROR_TEXTBOOK |

---

## 3. 正確洞回（入 DNA）

```text
L_empty = 外力除頭(L0) 同框
M       = kou(L0, L_empty) 凍 MARK
plate   = PATH1E / elev ref（native RATIO letterbox）
I_seat  = 外力生(base=L_empty, ref=plate)  # 只填洞
R       = hardpaste(L_empty 或 L0 規則, I_seat, M)  # outside=0 證
```

**禁：** freeframe 全圖當 I_seat 源再裁 M。

---

## 4. DNA 進化（自進化）

- PERSONA_KUANGYA_EXEC：禁 freeframe_hole_return · require seat_born_sheng
- F8 閘：`sheng_is_seat_born` 必 True；僅 outside=0 不足 PASS
- claim：污染未清前 ≤ C0_POLLUTED / C1
- 綁 STICK_XIN_NV_V2 錯教材為審查源

E：**E-POLLUTE-HOLE_RETURN_FREEFRAME**
