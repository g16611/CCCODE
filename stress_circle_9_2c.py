"""
9.2(c) 应力圆法：求主应力和主方向
单元体参数：σₓ = 50 MPa, σᵧ = 30 MPa, τₓᵧ = 0
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow

# ── 全局设置 ──────────────────────────────────────────────────────────────
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['text.usetex'] = False  # 用 matplotlib 内置 mathtext（无需 LaTeX 程序）

fig, ax = plt.subplots(figsize=(8, 7))

# ── 应力圆参数 ─────────────────────────────────────────────────────────────
sigma_x, sigma_y = 50, 30
tau_xy = 0
center = ((sigma_x + sigma_y) / 2, 0)   # (40, 0)
radius = np.sqrt(((sigma_x - sigma_y) / 2)**2 + tau_xy**2)  # 10

# ── 画坐标轴 ──────────────────────────────────────────────────────────────
sigma_min, sigma_max = 25, 55
tau_min, tau_max = -15, 15

# σ 轴（横轴）
ax.annotate('', xy=(sigma_max + 2, 0), xytext=(sigma_min - 2, 0),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
# τ 轴（纵轴）
ax.annotate('', xy=(0, tau_max + 2), xytext=(0, tau_min - 2),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))

# 轴标签
ax.text(sigma_max + 3, -2, r'$\sigma$ (MPa)', fontsize=14)
ax.text(-2, tau_max + 3, r'$\tau$ (MPa)', fontsize=14)
ax.text(0, -2, 'O', fontsize=12, ha='right')

# 刻度线 + 刻度值（σ 轴）
for s in range(25, 60, 5):
    ax.plot([s, s], [-0.5, 0.5], 'k', lw=1)
    if s % 10 == 0:
        ax.text(s, -2, str(s), fontsize=10, ha='center')

# 刻度线 + 刻度值（τ 轴）
for t in range(-15, 16, 5):
    if t == 0:
        continue
    ax.plot([-0.5, 0.5], [t, t], 'k', lw=1)
    ax.text(-2, t, str(t), fontsize=10, va='center', ha='right')

# ── 画应力圆 ───────────────────────────────────────────────────────────────
theta = np.linspace(0, 2 * np.pi, 200)
ax.plot(center[0] + radius * np.cos(theta),
        center[1] + radius * np.sin(theta),
        'b-', lw=2, label='应力圆')

# ── 标注圆心 ──────────────────────────────────────────────────────────────
ax.plot(center[0], center[1], 'ko', ms=5)
ax.text(center[0] + 0.8, center[1] - 2.5,
        r'$C(40, 0)$', fontsize=11, color='black')

# ── 标注四个关键点 ──────────────────────────────────────────────────────────
# A 点：α=0°（x 截面）  (σₓ, τₓᵧ) = (50, 0)
ax.plot(50, 0, 'ro', ms=7)
ax.annotate(r'A $\alpha=0^\circ$' + '\n' + r'$(50,\,0)$',
            xy=(50, 0), xytext=(52, -6),
            fontsize=10, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1),
            ha='center')

# B 点：α=90°（y 截面）  (σᵧ, −τₓᵧ) = (30, 0)
ax.plot(30, 0, 'ro', ms=7)
ax.annotate(r'B $\alpha=90^\circ$' + '\n' + r'$(30,\,0)$',
            xy=(30, 0), xytext=(28, -6),
            fontsize=10, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1),
            ha='center')

# D 点：α=45° 截面  (40, 10)  — 教材答案 σ_α=40, τ_α=10
ax.plot(40, 10, 'gs', ms=7)
ax.annotate(r'D $\alpha=45^\circ$' + '\n' + r'$(40,\,10)$',
            xy=(40, 10), xytext=(46, 10),
            fontsize=10, color='green',
            arrowprops=dict(arrowstyle='->', color='green', lw=1),
            ha='center')

# E 点：α=-45°（最大负切应力）(40, -10)
ax.plot(40, -10, 'gs', ms=7)
ax.annotate(r'E $\alpha=-45^\circ$' + '\n' + r'$(40,\,-10)$',
            xy=(40, -10), xytext=(46, -12),
            fontsize=10, color='green',
            arrowprops=dict(arrowstyle='->', color='green', lw=1),
            ha='center')

# ── 画半径 CA 和 CD，对比 α=0→45° 旋转 ────────────────────────────────────
ax.plot([center[0], 50], [0, 0], 'k--', lw=1)
ax.plot([center[0], 40], [0, 10], 'k-', lw=1.2, alpha=0.7)

# 画 2α = 90° 的弧（从 CA 到 CD）
arc_angle_start = 0
arc_angle_end = 90
arc_r = 3.5
arc_theta = np.linspace(np.radians(arc_angle_start), np.radians(arc_angle_end), 30)
ax.plot(center[0] + arc_r * np.cos(arc_theta),
        center[1] + arc_r * np.sin(arc_theta),
        'k-', lw=1.2)
ax.text(center[0] + 4.5, center[1] + 2.5, r'$2\alpha=90^\circ$',
        fontsize=10, color='black')

# ── 主应力标注（圆与 σ 轴交点即主应力） ────────────────────────────────────
ax.annotate(r'$\sigma_1=50$', xy=(50, 0), xytext=(55, 8),
            fontsize=12, color='red', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
ax.annotate(r'$\sigma_2=30$', xy=(30, 0), xytext=(22, 8),
            fontsize=12, color='red', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

# ── 标题 ──────────────────────────────────────────────────────────────────
ax.set_title(r'9.2(c) 应力圆 — $\sigma_x=50,\ \sigma_y=30,\ \tau_{xy}=0$',
             fontsize=14, pad=15)

# ── 网格和比例 ─────────────────────────────────────────────────────────────
ax.set_xlim(sigma_min - 3, sigma_max + 5)
ax.set_ylim(tau_min - 4, tau_max + 5)
ax.set_aspect('equal')
ax.grid(True, linestyle=':', alpha=0.4)

plt.tight_layout()
plt.savefig('/workspace/stress_circle_9_2c.png', dpi=150, bbox_inches='tight')
print("应力圆图已保存: /workspace/stress_circle_9_2c.png")
