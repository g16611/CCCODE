"""
9.2(c) 正确应力圆：σₓ=0, σᵧ=-20 MPa, τₓᵧ=50 MPa
教材答案校验：指定斜截面 α≈-33.7° 时 σ_α=40, τ_α=10
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['text.usetex'] = False

# ── 正确的原始应力 ────────────────────────────────────────────────────────
sigma_x = 0       # x 截面（左右竖直面）的正应力
sigma_y = -20     # y 截面（上下水平面）的正应力（压应力）
tau_xy  = 50      # 切应力（右面的 τ 向上 = +50）

center_sigma = (sigma_x + sigma_y) / 2          # -10
center_tau   = 0
radius       = np.sqrt(((sigma_x - sigma_y) / 2)**2 + tau_xy**2)  # sqrt(10^2+50^2)=sqrt(2600)≈50.99

sigma1 = center_sigma + radius    # ≈ 40.99
sigma2 = 0                        # z 方向
sigma3 = center_sigma - radius    # ≈ -60.99

print(f"圆心: ({center_sigma}, {center_tau})")
print(f"半径: {radius:.2f}")
print(f"主应力: σ₁={sigma1:.2f}, σ₂=0, σ₃={sigma3:.2f}")

# ── 画布 ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 8))

# ── 坐标轴 ───────────────────────────────────────────────────────────────
# σ 轴
ax.annotate('', xy=(70, 0), xytext=(-80, 0),
            arrowprops=dict(arrowstyle='->', lw=1.5))
# τ 轴
ax.annotate('', xy=(0, 70), xytext=(0, -70),
            arrowprops=dict(arrowstyle='->', lw=1.5))

ax.text(68, -4, r'$\sigma$ (MPa)', fontsize=14)
ax.text(-6, 68, r'$\tau$ (MPa)', fontsize=14)
ax.text(-3, -4, 'O', fontsize=12, ha='right')

# σ 轴刻度
for s in range(-80, 80, 20):
    ax.plot([s, s], [-1, 1], 'k', lw=0.8)
    ax.text(s, -4, str(s), fontsize=9, ha='center')
# τ 轴刻度
for t in range(-60, 70, 20):
    if t == 0:
        continue
    ax.plot([-1, 1], [t, t], 'k', lw=0.8)
    ax.text(-4, t, str(t), fontsize=9, va='center', ha='right')

# ── 应力圆 ────────────────────────────────────────────────────────────────
theta = np.linspace(0, 2 * np.pi, 300)
sig_circle = center_sigma + radius * np.cos(theta)
tau_circle = center_tau + radius * np.sin(theta)
ax.plot(sig_circle, tau_circle, 'b-', lw=2, label='stress circle')

# ── 圆心标注 ──────────────────────────────────────────────────────────────
ax.plot(center_sigma, center_tau, 'ko', ms=6)
ax.text(center_sigma - 2, center_tau - 5,
        f'C({center_sigma}, 0)', fontsize=11, color='black')

# ── 关键点 1：α=0°（x 截面，右面） (σₓ, τₓᵧ) = (0, 50) ────────────────
ax.plot(0, 50, 'ro', ms=8)
ax.annotate(r'A $\alpha=0^\circ$' + '\n' + r'$(0,\,50)$',
            xy=(0, 50), xytext=(20, 62),
            fontsize=10, color='red',
            arrowprops=dict(arrowstyle='->', color='red'),
            ha='center')

# ── 关键点 2：α=90°（y 截面，上面） (σᵧ, -τₓᵧ) = (-20, -50) ──────────
ax.plot(-20, -50, 'ro', ms=8)
ax.annotate(r'B $\alpha=90^\circ$' + '\n' + r'$(-20,\,-50)$',
            xy=(-20, -50), xytext=(-50, -62),
            fontsize=10, color='red',
            arrowprops=dict(arrowstyle='->', color='red'),
            ha='center')

# ── 主应力点（圆与 σ 轴交点） ─────────────────────────────────────────────
# σ₁ ≈ 40.99（圆右交点）
ax.plot(sigma1, 0, 'r*', ms=14)
ax.annotate(r'$\sigma_1 \approx 41$', xy=(sigma1, 0), xytext=(52, 10),
            fontsize=12, color='red', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

# σ₃ ≈ -60.99（圆左交点）
ax.plot(sigma3, 0, 'r*', ms=14)
ax.annotate(r'$\sigma_3 \approx -61$', xy=(sigma3, 0), xytext=(-80, 10),
            fontsize=12, color='red', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

# σ₂ = 0（z 方向，平面外）
ax.text(-4, -20, r'$\sigma_2 = 0$ (out-of-plane)',
        fontsize=10, color='gray', fontstyle='italic')

# ── 教材答案验证点：解出 2α ≈ -67.38° (α ≈ -33.69°) → σ=40, τ=10 ─────
# 方程: A+5B=1, A²+B²=1 → A=sin2α=-12/13, B=cos2α=5/13
two_alpha = np.degrees(np.arctan2(-12, 5))          # ≈ -67.38°
alpha_sol = two_alpha / 2                            # ≈ -33.69°
sigma_at_alpha = -10 + 10 * np.cos(np.radians(two_alpha)) - 50 * np.sin(np.radians(two_alpha))
tau_at_alpha   =  10 * np.sin(np.radians(two_alpha)) + 50 * np.cos(np.radians(two_alpha))
print(f"验证点 2α={two_alpha:.2f}°, α={alpha_sol:.2f}°: σ={sigma_at_alpha:.2f}, τ={tau_at_alpha:.2f}")

ax.plot(sigma_at_alpha, tau_at_alpha, 'gs', ms=9)
ax.annotate(r'D $\alpha \approx -33.7^\circ$' + f'\n({sigma_at_alpha:.1f}, {tau_at_alpha:.1f})',
            xy=(sigma_at_alpha, tau_at_alpha), xytext=(60, 35),
            fontsize=10, color='green',
            arrowprops=dict(arrowstyle='->', color='green'),
            ha='center')

# ── 画半径 CA（基准 α=0°）和 CD（α=-33.7°），标 2α 弧 ───────────────────
ax.plot([center_sigma, 0], [center_tau, 50], 'k--', lw=1)
ax.plot([center_sigma, sigma_at_alpha], [center_tau, tau_at_alpha], 'k-', lw=1.2, alpha=0.7)

# 2α ≈ -67.38° 的弧
arc_r = 6
arc_theta_vals = np.linspace(np.radians(0), np.radians(two_alpha), 40)
ax.plot(center_sigma + arc_r * np.cos(arc_theta_vals),
        center_tau + arc_r * np.sin(arc_theta_vals),
        'k-', lw=1.2)
ax.text(center_sigma + 10, center_tau + 2,
        r'$2\alpha \approx -67.4^\circ$', fontsize=10)

# ── 切应力符号说明 ────────────────────────────────────────────────────────
ax.text(-75, 60, r'$+\tau$ (counterclockwise on right face)',
        fontsize=9, color='gray', ha='left')
ax.text(-75, -60, r'$-\tau$ (clockwise on right face)',
        fontsize=9, color='gray', ha='left')

# ── 标题 ──────────────────────────────────────────────────────────────────
ax.set_title(
    r'9.2(c) Stress Circle — $\sigma_x=0,\ \sigma_y=-20,\ \tau_{xy}=50$ MPa',
    fontsize=13, pad=14)

ax.set_xlim(-85, 75)
ax.set_ylim(-70, 72)
ax.set_aspect('equal')
ax.grid(True, linestyle=':', alpha=0.4)

plt.tight_layout()
plt.savefig('/workspace/stress_circle_9_2c_v2.png', dpi=150, bbox_inches='tight')
print("应力圆图已保存: /workspace/stress_circle_9_2c_v2.png")
