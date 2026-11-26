"""
9.2(c) 主单元体绘制（清理版：标注全部移到图形外侧，避免重叠）
原始应力: sigma_x = 0, sigma_y = -20 MPa, tau_xy = +50 MPa
主应力 : sigma_1 ≈ 41.0, sigma_2 = 0, sigma_3 ≈ -61.0 MPa
主方向 : alpha_p1 ≈ -39.3°（sigma_1 方向，自 x 轴顺时针）
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['text.usetex'] = False

# ---------------- mechanics ----------------
sx, sy, txy = 0.0, -20.0, 50.0
c = (sx + sy) / 2.0
R = np.hypot((sx - sy) / 2.0, txy)
s1, s3 = c + R, c - R
ap = 0.5 * np.degrees(np.arctan2(-2.0 * txy, sx - sy))   # sigma_1 direction
ap3 = ap + 90.0

print(f"center = {c:.2f}, R = {R:.2f}")
print(f"sigma_1 = {s1:.2f}, sigma_3 = {s3:.2f}")
print(f"alpha_p1 = {ap:.2f} deg, alpha_p3 = {ap3:.2f} deg")

fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.5, 6.6))
for ax, xl in ((axL, 2.75), (axR, 3.30)):
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-xl, xl)
    ax.set_ylim(-2.45, 2.45)

WB = dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.92)


def arr(ax, p0, p1, color='k', lw=2.0, ms=16):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw,
                                mutation_scale=ms))

# ======================= LEFT: original element =======================
a = 1.0
axL.add_patch(Polygon([(-a, -a), (a, -a), (a, a), (-a, a)], closed=True,
                      facecolor='#f2f2f2', edgecolor='k', lw=2.2))

# sigma_y = -20 MPa（压应力，箭头指向面内）
arr(axL, (0, 1.62), (0, 1.0), '#c00000')
arr(axL, (0, -1.62), (0, -1.0), '#c00000')
axL.text(0, 1.72, r'$\sigma_y=-20$ MPa', color='#c00000',
         ha='center', va='bottom', fontsize=11)
axL.text(0, -1.72, r'$\sigma_y=-20$ MPa', color='#c00000',
         ha='center', va='top', fontsize=11)

# tau_xy = +50 MPa（右面向上、左面向下）
arr(axL, (a, -0.55), (a, 0.55), '#1f4e79')
arr(axL, (-a, 0.55), (-a, -0.55), '#1f4e79')
axL.text(1.10, 0.66, r'$\tau_{xy}=+50$ MPa', color='#1f4e79',
         ha='left', va='bottom', fontsize=11)

# sigma_x = 0（左右竖直面无水平正应力）
axL.text(-1.14, 0.64, r'$\sigma_x=0$', color='#555555',
         ha='right', va='bottom', fontsize=11, bbox=WB)

# 主方向（虚线）
th = np.radians(ap)
th3 = th + np.pi / 2
L = 1.80
axL.plot([-L * np.cos(th), L * np.cos(th)],
         [-L * np.sin(th), L * np.sin(th)], '--', color='#2e7d32', lw=1.6)
axL.plot([-L * np.cos(th3), L * np.cos(th3)],
         [-L * np.sin(th3), L * np.sin(th3)], '--', color='#ef6c00', lw=1.6)

axL.text(1.44, -1.24, r'$\sigma_1$ dir', color='#2e7d32',
         ha='left', va='center', fontsize=10.5, bbox=WB)
axL.text(1.10, 1.52, r'$\sigma_3$ dir', color='#ef6c00',
         ha='left', va='bottom', fontsize=10.5, bbox=WB)

axL.text(0, -2.10,
         r'$\sigma_x=0,\ \ \sigma_y=-20$ MPa, $\ \tau_{xy}=+50$ MPa',
         ha='center', va='center', fontsize=10.5, color='#333333')
axL.text(0, -2.33,
         r'principal directions: $\alpha_{p1}=-39.3^\circ$, $\alpha_{p3}=50.7^\circ$',
         ha='center', va='center', fontsize=10, color='#333333')
axL.set_title('(c) Original element', fontsize=13, pad=12)

# ======================= RIGHT: principal element =======================
e1 = np.array([np.cos(th), np.sin(th)])      # sigma_1 轴
e2 = np.array([-np.sin(th), np.cos(th)])     # sigma_3 轴

axR.add_patch(Polygon([a * e1 + a * e2, -a * e1 + a * e2,
                       -a * e1 - a * e2, a * e1 - a * e2], closed=True,
                      facecolor='#eef5ee', edgecolor='k', lw=2.2))

# sigma_1 拉应力：箭头沿 +-e1 向外
arr(axR, a * e1, 1.65 * e1, '#2e7d32')
arr(axR, -a * e1, -1.65 * e1, '#2e7d32')
# sigma_3 压应力：箭头沿 +-e2 向内
arr(axR, 1.65 * e2, a * e2, '#ef6c00')
arr(axR, -1.65 * e2, -a * e2, '#ef6c00')

# 标注一律放在箭杆延长线之外
p = 1.85 * e1
axR.text(p[0], p[1], r'$\sigma_1=41.0$', color='#2e7d32',
         ha='left', va='center', fontsize=11, bbox=WB)
p = -1.85 * e1
axR.text(p[0], p[1], r'$\sigma_1=41.0$', color='#2e7d32',
         ha='right', va='center', fontsize=11, bbox=WB)
p = 2.00 * e2 - 0.16 * e1
axR.text(p[0], p[1], r'$\sigma_3=-61.0$', color='#ef6c00',
         ha='left', va='bottom', fontsize=11, bbox=WB)
p = -2.00 * e2 + 0.16 * e1
axR.text(p[0], p[1], r'$\sigma_3=-61.0$', color='#ef6c00',
         ha='right', va='top', fontsize=11, bbox=WB)

# x 轴指示
axR.annotate('', xy=(2.75, 0.0), xytext=(2.15, 0.0),
             arrowprops=dict(arrowstyle='->', lw=1.0, color='gray'))
axR.text(2.82, 0.0, r'$x$', fontsize=10, va='center', color='gray')

axR.text(0, -2.10,
         r'$\sigma_1$ (tension), $\ \sigma_3$ (compression), $\ \sigma_2=0$ (z)',
         ha='center', va='center', fontsize=10.5, color='#333333')
axR.text(0, -2.33,
         r'element rotated by $\alpha_{p1}=-39.3^\circ$',
         ha='center', va='center', fontsize=10, color='#333333')
axR.set_title('Principal element (MPa)', fontsize=13, pad=12)

plt.tight_layout()
plt.savefig('/workspace/principal_element_9_2c.png', dpi=150, bbox_inches='tight')
print("saved: /workspace/principal_element_9_2c.png")
