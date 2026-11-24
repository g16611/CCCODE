"""
9.2(c) 主单元体绘制
原始应力: sigma_x = 0, sigma_y = -20 MPa, tau_xy = +50 MPa
主应力 : sigma_1 ≈ 41.0, sigma_2 = 0, sigma_3 ≈ -61.0 MPa
主方向 : alpha_p1 ≈ -39.34° (自 x 轴顺时针)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc

plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['text.usetex'] = False

# ---------------- mechanics ----------------
sx, sy, txy = 0.0, -20.0, 50.0
c = (sx + sy) / 2.0
R = np.hypot((sx - sy) / 2.0, txy)
s1, s3 = c + R, c - R
ap = 0.5 * np.degrees(np.arctan2(-2.0 * txy, sx - sy))   # sigma_1 direction

print(f"center = {c:.2f}, R = {R:.2f}")
print(f"sigma_1 = {s1:.2f}, sigma_3 = {s3:.2f}, alpha_p1 = {ap:.2f} deg")

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.5, 6.4))
for ax in (axL, axR):
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.4, 2.4)


def arr(ax, p0, p1, color='k', lw=1.8, ms=14):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw,
                                mutation_scale=ms))

# ======================= LEFT: original element =======================
a = 1.0
axL.add_patch(Polygon([(-a, -a), (a, -a), (a, a), (-a, a)], closed=True,
                      facecolor='#f2f2f2', edgecolor='k', lw=2))

# tau_xy: right face up, left face down
arr(axL, (a, -0.55), (a, 0.55), color='#1f4e79')
arr(axL, (-a, 0.55), (-a, -0.55), color='#1f4e79')
axL.text(a + 0.08, 0.70, r'$\tau_{xy}=50$ MPa', color='#1f4e79', fontsize=12)

# sigma_y compression (arrows push into faces)
arr(axL, (0, a + 0.55), (0, a), color='#c00000')
arr(axL, (0, -a - 0.55), (0, -a), color='#c00000')
axL.text(0.0, a + 0.75, r'$\sigma_y=-20$ MPa', color='#c00000',
         fontsize=12, ha='center')

# sigma_x = 0
axL.text(-a - 0.10, -0.20, r'$\sigma_x=0$', fontsize=11, ha='right',
         color='#555555')

# principal directions (dashed)
th = np.radians(ap)
L = 1.72
axL.plot([-L * np.cos(th), L * np.cos(th)],
         [-L * np.sin(th), L * np.sin(th)], '--', color='#2e7d32', lw=1.5)
th3 = th + np.pi / 2
axL.plot([-L * np.cos(th3), L * np.cos(th3)],
         [-L * np.sin(th3), L * np.sin(th3)], '--', color='#ef6c00', lw=1.5)

# angle arc from +x to sigma_1 direction
axL.add_patch(Arc((0, 0), 1.25, 1.25, angle=0, theta1=ap, theta2=0,
                  color='k', lw=1.1))
axL.text(0.72 * np.cos(np.radians(ap / 2)) + 0.02,
         0.72 * np.sin(np.radians(ap / 2)) - 0.16,
         r'$\alpha_{p}=-39.3^\circ$', fontsize=10)

axL.text(1.18 * np.cos(th) + 0.12, 1.18 * np.sin(th) - 0.30,
         r'$\sigma_1$ dir', color='#2e7d32', fontsize=10)
axL.text(1.10 * np.cos(th3) - 0.85, 1.10 * np.sin(th3) + 0.10,
         r'$\sigma_3$ dir', color='#ef6c00', fontsize=10)

axL.text(0, -2.20, r'original: $\sigma_x=0,\ \sigma_y=-20,\ \tau_{xy}=50$ MPa',
         fontsize=11, ha='center', color='#333333')
axL.set_title('(c) Original element', fontsize=13)

# ======================= RIGHT: principal element =======================
e1 = np.array([np.cos(th), np.sin(th)])      # sigma_1 axis
e2 = np.array([-np.sin(th), np.cos(th)])     # sigma_3 axis

axR.add_patch(Polygon([a * e1 + a * e2, -a * e1 + a * e2,
                       -a * e1 - a * e2, a * e1 - a * e2], closed=True,
                      facecolor='#eef5ee', edgecolor='k', lw=2))

# sigma_1 tension: arrows point outward along +-e1
arr(axR, a * e1, (a + 0.62) * e1, color='#2e7d32', lw=2)
arr(axR, -a * e1, -(a + 0.62) * e1, color='#2e7d32', lw=2)
# sigma_3 compression: arrows point inward along +-e2
arr(axR, (a + 0.62) * e2, a * e2, color='#ef6c00', lw=2)
arr(axR, -(a + 0.62) * e2, -a * e2, color='#ef6c00', lw=2)

# labels near arrow tips
axR.text(1.42 * e1[0] + 0.02, 1.42 * e1[1] - 0.32,
         r'$\sigma_1\!\approx\!41.0$ MPa', color='#2e7d32', fontsize=11,
         ha='left', va='top')
axR.text(-1.30 * e1[0] - 0.05, -1.30 * e1[1] + 0.30,
         r'$\sigma_1\!\approx\!41.0$ MPa', color='#2e7d32', fontsize=11,
         ha='right', va='bottom')
axR.text(1.08 * e2[0] + 0.06, 1.08 * e2[1] + 0.10,
         r'$\sigma_3\!\approx\!-61.0$ MPa', color='#ef6c00', fontsize=11,
         ha='left', va='bottom')
axR.text(-1.08 * e2[0] - 0.06, -1.08 * e2[1] - 0.12,
         r'$\sigma_3\!\approx\!-61.0$ MPa', color='#ef6c00', fontsize=11,
         ha='right', va='top')

# small x-axis indicator + rotation note
axR.annotate('', xy=(2.05, 0.0), xytext=(1.45, 0.0),
             arrowprops=dict(arrowstyle='->', lw=1.0, color='gray'))
axR.text(2.10, 0.0, r'$x$', fontsize=10, va='center', color='gray')

axR.text(0, -2.20, r'rotated by $\alpha_{p1}=-39.3^\circ$;  $\sigma_2=0$ (z, out of plane)',
         fontsize=11, ha='center', color='#333333')
axR.set_title('Principal element', fontsize=13)

plt.tight_layout()
plt.savefig('/workspace/principal_element_9_2c.png', dpi=150, bbox_inches='tight')
print("saved: /workspace/principal_element_9_2c.png")
