
# 回洞升清比例 · formal HOLE_RETURN_SCALE_V1

## 符號
- 洞尺 hole：$(W_h, H_h)$ = MARK bbox 寬高（框標）
- 框標 frame：$(x_0,y_0,x_1,y_1),\; c=(c_x,c_y),\; pad$
- 放大圖 elev/S6：$(W_e, H_e)$
- peep 金：$(W_p, H_p)$ · 與洞同構 asp
- 虛擬根因 $k$：域縮放（SS驗 clusters）

## 根因係數（虛擬預設，可被 SS驗實測覆寫）
$$
k_{\mathrm{S0A}}=\frac{H_{\mathrm{S0A}}}{H_{\mathrm{S0}}},\quad
k_{\mathrm{peep}}=\frac{H_p}{H_{\mathrm{S0A}}},\quad
k_{\mathrm{zoom}}=\frac{H_e}{H_p}
$$

## 回洞正確比例（升清）
1) 先把放大圖折回 peep 等效（消 zoom 根因）：
$$
(W_e', H_e') = \Big(\frac{W_e}{k_{\mathrm{zoom}}}, \frac{H_e}{k_{\mathrm{zoom}}}\Big)
\;\approx\;(W_p, H_p)
$$
2) 洞目標尺 = 框標洞：
$$
(W^\star, H^\star) = (W_h, H_h)
$$
3) 升清回洞縮放（金 · 分別軸對洞 · 比例鎖 peep/洞 asp）：
$$
s_x = \frac{W_h}{W_e},\quad s_y = \frac{H_h}{H_e}
$$
等比備選：
$$
s_{\mathrm{fit}}=\min(s_x,s_y),\quad
s_{\mathrm{cover}}=\max(s_x,s_y)
$$
4) 置中硬貼：
$$
I_{\mathrm{hole}}(x,y)=
\begin{cases}
\mathrm{resize}(I_e,(W_h,H_h))(x-x_0,y-y_0) & (x,y)\in\mathrm{MARK}\\
I_{\mathrm{base}} & \text{else}
\end{cases}
$$
5) SS驗閘：outside$(I_{\mathrm{ret}},I_{\mathrm{S0}},M)=0$ 且 $S7\times S5$ size_lock

## 禁
- 用 freeframe 全圖尺當洞尺
- 用 S6 尺直接 hardpaste 不除 $k_{\mathrm{zoom}}$
- elev 冒 RETURN
