# SS驗 V2

**call**: `SS驗` · **formal**: `SHQ_SS_YAN_V2_INPAINT_SEAT_V1` · **stick**: `STICK_SS_YAN_V2`

## 一句
同域对位硬闸 + 回洞值表 + 外力GROK只许洞座INPAINT升清 + 禁freeframe；3D SS为伴生名

## 方程
```
SS驗_V2 = ∀同域(Si×Sj): size_lock ∧ outside(M)=0 ∧ RATIO(peep,洞) ∧ 回洞 s_x=Wh/We,s_y=Hh/He (值表可冻) ∧ 生 = INPAINT@MARK (非 freeframe elev) ∧ elev≠RETURN ∧ S11×S0 锁
```

## 新闸（相对 01531）
- **G7** 升清 = 洞座 INPAINT @ MARK（freeframe elev = BAN / E-SS-08）
- **G8** pose lock |dx|+|dy|≤1 vs 金位
- **G9** 回洞值表 Wh,Hh,sx,sy,k_zoom,bbox

## 金链
- S0 冻
- S0A 子集工域
- S1 外力除
- S2 扣
- S3 洞 MARK
- S5 peep0 金位
- S6 放大暂态 (可值表)
- S7 仅 peep 尺子；真升清=INPAINT@洞
- S8 BOOST
- S9 生 = hard(S0A, INPAINT⊙M)
- S10 hardpaste
- S11 工域反 outside=0
- S01 map 值表 bbox → 母帧

## 伴生
- **3D SS**：硬闸通过后的微残差立体感命名，不替代 SS驗

ACCEPT_FULL_HD = false
