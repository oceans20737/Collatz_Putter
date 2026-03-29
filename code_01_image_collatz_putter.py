# Copyright (c) 2026 Hiroshi Harada
# Licensed under the MIT License.
# Base-3 Putter Shot: Friction Dynamics Visualizer (Static Final, FIXED)
# Author: Hiroshi Harada
# Date: March 29, 2026

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
import matplotlib.cm as cm

# ---------------------------------------------------------
#  Safe numerical utilities
# ---------------------------------------------------------

def safe_log3(n):
    if n <= 0: return 0.0
    b = n.bit_length()
    if b < 1000:
        return np.log(float(n)) / np.log(3.0)
    e = b - 60
    m = n >> e
    return (np.log(float(m)) + e * np.log(2.0)) / np.log(3.0)

def safe_div_to_float(num, den):
    if den == 0: return 0.0
    shift = max(0, max(num.bit_length(), den.bit_length()) - 1000)
    return float(num >> shift) / float(den >> shift)

# ---------------------------------------------------------
#  Shiftless Collatz Dynamics
# ---------------------------------------------------------

def collatz_shiftless_coupled_putter(seed):
    a_k = int(seed)
    b_k = 0
    history = []

    while True:
        n_k = a_k + b_k
        if n_k > 0 and (n_k & (n_k - 1)) == 0:
            break

        lsb = n_k & -n_k
        a_next = a_k * 3
        b_next = b_k * 3 + lsb
        mu = safe_div_to_float(lsb, b_next)

        history.append({'n': n_k, 'mu': mu})
        a_k, b_k = a_next, b_next

    final_n = a_k + b_k
    history.append({'n': final_n, 'mu': 0.0})
    return history

def n_to_polar_b3(n_list):
    if isinstance(n_list, (int, float)): n_list = [n_list]
    rs = np.array([safe_log3(x) for x in n_list])
    theta = (2 * np.pi * (rs % 1.0)) % (2 * np.pi)
    return rs, theta

# ---------------------------------------------------------
#  Simulation
# ---------------------------------------------------------

seed = 27
history = collatz_shiftless_coupled_putter(seed)

ns = [h['n'] for h in history]
mus = [h['mu'] for h in history[:-1]]

rs, thetas = n_to_polar_b3(ns)

mus_val = np.array(mus)
log_mus = np.log10(np.where(mus_val <= 0, 1e-15, mus_val))
norm_mus = (log_mus - log_mus.min()) / (log_mus.max() - log_mus.min())

# ---------------------------------------------------------
#  Plotting
# ---------------------------------------------------------

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(14, 14))
green_bg = '#144324'
fig.patch.set_facecolor(green_bg)
ax.set_facecolor(green_bg)

fig.subplots_adjust(right=0.75, top=0.85)

max_n = max(ns)
max_exp = max_n.bit_length() + 5
step = max(1, max_exp // 2000)
cups_n = [1 << i for i in range(0, max_exp, step)]

r_cups, theta_cups = n_to_polar_b3(cups_n)
ax.scatter(theta_cups, r_cups, color='#ffffff', s=20, alpha=0.2, linewidths=0, zorder=2)

cool_map = cm.cool

for i in range(len(history) - 1):
    color = cool_map(norm_mus[i])
    lw = 1.0 + norm_mus[i] * 8.0
    ax.plot(thetas[i:i+2], rs[i:i+2], color=color, linewidth=lw, alpha=0.8, zorder=10)

ax.scatter(thetas, rs, c=np.arange(len(rs)), cmap='cool', s=45, edgecolors='white', lw=0.5, zorder=11)

f_r, f_t = rs[-1], thetas[-1]
final_n = ns[-1]
jackpot_exponent = final_n.bit_length() - 1

pole_len = 4.0
ax.plot([f_t, f_t], [f_r, f_r + pole_len], color='#ffffff', lw=3, zorder=20,
        path_effects=[patheffects.withStroke(linewidth=5, foreground='black')])

flag_top = f_r + pole_len
flag_r = [flag_top, flag_top - 0.5, flag_top - 1.0, flag_top - 1.5]
flag_t = [f_t, f_t + 0.18, f_t + 0.08, f_t]
ax.fill(flag_t, flag_r, color='yellow', alpha=1.0, zorder=21,
        path_effects=[patheffects.withStroke(linewidth=1.5, foreground='black')])

ax.scatter(f_t, f_r, color='#ffff00', s=500, marker='*', edgecolors='white', lw=2, zorder=15)

ax.set_theta_zero_location("N")
ax.set_theta_direction(1)
ax.set_rlabel_position(0)
ax.grid(True, color='white', alpha=0.1)

xticks = np.arange(0, 2 * np.pi, np.pi / 4)
ax.set_xticks(xticks)
ax.set_xticklabels([r'0', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$',
                    r'$\pi$', r'$\frac{5\pi}{4}$', r'$\frac{3\pi}{2}$', r'$\frac{7\pi}{4}$'], color='#88bb99')

ticks = np.arange(0, rs.max() + 5, 5)
ax.set_rticks(ticks)
ax.set_yticklabels([f"$3^{{{int(t)}}}$" for t in ticks], color='#ffffff', alpha=0.8, fontsize=12)

ax.annotate(f"Cup-in!\n$2^{{{jackpot_exponent}}}$",
            xy=(f_t, f_r), xytext=(-80, -80), textcoords='offset points',
            color='white', fontsize=18, fontweight='bold', ha='right',
            arrowprops=dict(arrowstyle="->", color='white', connectionstyle="arc3,rad=-.2", lw=2))

plt.suptitle(
    f"Base-3 Putter Shot in the Shiftless Collatz Model\nSeed: {seed} → Jackpot: $2^{{{jackpot_exponent}}}$",
    color='white', fontsize=24, fontweight='bold', y=0.98
)

# ---------------------------------------------------------
#  Legend, FIXED
# ---------------------------------------------------------
sc_Trajectory_legend = plt.Line2D([0], [0], color=cool_map(0.9), lw=4, label='Trajectory colored by friction')
sc_wake_legend = plt.Line2D([0], [0], color='none', marker='o', markerfacecolor=cool_map(0.5), markeredgecolor='white', markersize=8, label='Ball Wake')
flag_legend = plt.Line2D([0], [0], color='yellow', marker='*', markeredgecolor='black', markersize=12, linestyle='none', label=f'Jackpot Impact ($2^{{{jackpot_exponent}}}$)')
sc_cups_legend = plt.Line2D([0], [0], color='none', marker='o', markerfacecolor='#ffffff', markeredgecolor='none', markersize=5, alpha=0.2, label='Potential Cup wells')

handles = [sc_Trajectory_legend, sc_wake_legend, flag_legend, sc_cups_legend]

legend = ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1.05, 0.5),
                   facecolor='#1a1a1a', edgecolor='#444444', framealpha=0.9, fontsize=12, labelcolor='white')
plt.setp(legend.get_title(), color='white')

# ---------------------------------------------------------
#  PNG
# ---------------------------------------------------------
output_filename = f"image_b3_putter_shot_seed_{seed}.png"
plt.savefig(output_filename, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
print(f"✨ Saved static image: {output_filename}")

plt.show()

