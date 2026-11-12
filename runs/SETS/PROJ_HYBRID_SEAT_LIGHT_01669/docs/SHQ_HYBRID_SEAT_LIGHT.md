# 合取·座光 01669

## 各取
| 源 | 取 |
|----|----|
| A 593b S11 | 茶壶 **镂空重贴** hardpaste |
| B f704 B1正 | **空间光** + **人/衣** 质感 |

## 式
```
R = B                          # 光与人质感底
R = hardpaste(R, A, M_teapot)  # 壶座主权
R = hardpaste(R, B, M_person)  # 人强制 B
(+ 挂锅区微结构 0.35 可选)
```

## BAN
全图 0.5 均混

PASS=True teapot_vs_A=0 person_vs_B=0
