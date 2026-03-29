# Copyright (c) 2026 Hiroshi Harada
# Licensed under the MIT License.
# Base-3 Putter Shot: Animated Visualizer
# Author: Hiroshi Harada
# Date: March 29, 2026

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as patheffects
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
import shutil
from tqdm import tqdm

try:
    from IPython.display import HTML, display
    in_jupyter = True
except ImportError:
    in_jupyter = False


# ---------------------------------------------------------
#  Safe Math Utilities
# ---------------------------------------------------------

def safe_log3(n):
    if n <= 0:
        return 0.0
    b = n.bit_length()
    if b < 1000:
        return np.log(float(n)) / np.log(3.0)
    e = b - 60
    m = n >> e
    return (np.log(float(m)) + e * np.log(2.0)) / np.log(3.0)


def safe_div_to_float(num, den):
    if den == 0:
        return 0.0
    shift = max(0, max(num.bit_length(), den.bit_length()) - 1000)
    return float(num >> shift) / float(den >> shift)


# ---------------------------------------------------------
#  Shiftless Collatz Dynamics
# ---------------------------------------------------------

def collatz_shiftless_coupled_putter(seed):
    a_k, b_k = int(seed), 0
    history = []

    while True:
        n_k = a_k + b_k

        # Jackpot: perfect power of 2
        if n_k > 0 and (n_k & (n_k - 1)) == 0:
            break

        lsb = n_k & -n_k
        a_next = a_k * 3
        b_next = b_k * 3 + lsb

        mu = safe_div_to_float(lsb, b_next)
        history.append({'n': n_k, 'mu': mu})

        a_k, b_k = a_next, b_next

    history.append({'n': a_k + b_k, 'mu': 0.0})
    return history


# ---------------------------------------------------------
#  Base-3 Log Spiral Mapping
# ---------------------------------------------------------

def n_to_polar_b3(n_list):
    if isinstance(n_list, (int, float)):
        n_list = [n_list]
    rs = np.array([safe_log3(x) for x in n_list])
    theta = (2 * np.pi * (rs % 1.0)) % (2 * np.pi)
    return rs, theta


# ---------------------------------------------------------
#  Simulation Setup
# ---------------------------------------------------------

seed = 27
history = collatz_shiftless_coupled_putter(seed)

ns = [h['n'] for h in history]
mus = [h['mu'] for h in history[:-1]]

rs, thetas = n_to_polar_b3(ns)

log_mus = np.log10(np.where(np.array(mus) <= 0, 1e-15, mus))
norm_mus = (log_mus - log_mus.min()) / (log_mus.max() - log_mus.min())


# ---------------------------------------------------------
#  Canvas Setup
# ---------------------------------------------------------

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(14, 14))
green_bg = '#144324'
fig.patch.set_facecolor(green_bg)
ax.set_facecolor(green_bg)
fig.subplots_adjust(right=0.75)

max_exp = max(ns).bit_length() + 5
cups_n = [1 << i for i in range(0, max_exp, max(1, max_exp // 1000))]
r_cups, theta_cups = n_to_polar_b3(cups_n)

ax.scatter(theta_cups, r_cups, color='#ffffff', s=20, alpha=0.2,
           linewidths=0, zorder=2)

ax.set_theta_zero_location("N")
ax.set_theta_direction(1)
ax.set_rlabel_position(0)
ax.grid(True, color='white', alpha=0.1)

xticks = np.arange(0, 2 * np.pi, np.pi / 4)
ax.set_xticks(xticks)
ax.set_xticklabels(
    [r'0', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$',
     r'$\pi$', r'$\frac{5\pi}{4}$', r'$\frac{3\pi}{2}$', r'$\frac{7\pi}{4}$'],
    color='#88bb99'
)

ticks_r = np.arange(0, rs.max() + 5, 5)
ax.set_rticks(ticks_r)
ax.set_yticklabels([f"$3^{{{int(t)}}}$" for t in ticks_r],
                   color='#ffffff', alpha=0.6)

ax.set_rmax(rs.max() + 8.0)
ax.autoscale(False)

jackpot_exponent = ns[-1].bit_length() - 1

plt.suptitle(
    f"Base-3 Putter Shot in the Shiftless Collatz Model\n(Animated, Seed: {seed})",
    color='#ffd700', fontsize=24, fontweight='bold', y=0.95
)

cool_map = cm.cool

# Legend
sc_Trajectory_legend = plt.Line2D([0], [0], color=cool_map(0.9), lw=4,
                                  label='Trajectory colored by friction')
sc_ball_legend = plt.Line2D([0], [0], color='none', marker='o',
                            markerfacecolor=cool_map(0.5),
                            markeredgecolor='white', markersize=10,
                            label='Ball Position')
flag_legend = plt.Line2D([0], [0], color='yellow', marker='*',
                         markeredgecolor='black', markersize=12,
                         linestyle='none',
                         label=f'Jackpot Impact ($2^{{{jackpot_exponent}}}$)')
sc_cups_legend = plt.Line2D([0], [0], color='none', marker='o',
                            markerfacecolor='#ffffff', markeredgecolor='none',
                            markersize=5, alpha=0.8,
                            label='Potential Cup wells')

handles = [sc_Trajectory_legend, sc_ball_legend, flag_legend, sc_cups_legend]

legend = ax.legend(handles=handles, loc='center left',
                   bbox_to_anchor=(1.05, 0.5),
                   facecolor='#1a1a1a', edgecolor='#444444',
                   framealpha=0.9, fontsize=12)

for text in legend.get_texts():
    text.set_color('white')

ball, = ax.plot([], [], 'o', markersize=12,
                markeredgecolor='white', zorder=15)

dynamic_elements = []


# ---------------------------------------------------------
#  Animation Update Function
# ---------------------------------------------------------

def update(frame):
    global dynamic_elements

    if frame == 0:
        for el in dynamic_elements:
            el.remove()
        dynamic_elements.clear()

    step = min(frame, len(rs) - 1)

    ball.set_data([thetas[step]], [rs[step]])
    ball.set_color(cool_map(step / len(rs)))

    if 0 < frame < len(rs):
        c = cool_map(norm_mus[step - 1])
        w = 1.0 + norm_mus[step - 1] * 8.0
        line, = ax.plot(thetas[step - 1:step + 1], rs[step - 1:step + 1],
                        color=c, linewidth=w, alpha=0.8, zorder=10)
        dynamic_elements.append(line)

    if frame == len(rs) - 1:
        f_r, f_t = rs[-1], thetas[-1]

        pole, = ax.plot([f_t, f_t], [f_r, f_r + 4.0],
                        color='#aaaaaa', linewidth=5, zorder=20,
                        path_effects=[patheffects.withStroke(
                            linewidth=5, foreground='black')])
        dynamic_elements.append(pole)

        flag_r = [f_r + 4.0, f_r + 3.5, f_r + 3.0, f_r + 2.5]
        flag_t = [f_t, f_t + 0.18, f_t + 0.08, f_t]
        patches = ax.fill(flag_t, flag_r, color='#ffec00',
                          alpha=1.0, zorder=21,
                          path_effects=[patheffects.withStroke(
                              linewidth=1.5, foreground='black')])
        dynamic_elements.extend(patches)

        star = ax.scatter(f_t, f_r, color='#ffff00', s=600,
                          marker='*', edgecolors='white',
                          lw=2, zorder=15)
        dynamic_elements.append(star)

        anno = ax.annotate(
            f"Cup-in!\n$2^{{{jackpot_exponent}}}$",
            xy=(f_t, f_r), xytext=(-60, 40),
            textcoords='offset points',
            color='white', fontsize=16,
            ha='left', va='bottom', zorder=25,
            bbox=dict(boxstyle="round", fc=green_bg,
                      ec="white", lw=2, alpha=0.9),
            arrowprops=dict(arrowstyle="->", color='white',
                            connectionstyle="arc3,rad=-.2", lw=2)
        )
        dynamic_elements.append(anno)

    return ball,


# ---------------------------------------------------------
#  Animation Object
# ---------------------------------------------------------

total_steps = len(rs)
pause_frames = 4
total_frames = total_steps + pause_frames
fps_setting = 2

ani = FuncAnimation(fig, update, frames=total_frames,
                    interval=600, blit=False, repeat=False)

output_name = f"animation_b3_putter_shot_seed_{seed}"


# ---------------------------------------------------------
#  Export (MP4 + GIF)
# ---------------------------------------------------------

if shutil.which('ffmpeg'):
    print(f"🎯 Starting MP4 Hunt... (Seed: {seed}, Total Frames: {total_frames})")
    try:
        with tqdm(total=total_frames, desc="MP4 Encoding") as pbar:
            ani.save(
                f"{output_name}.mp4",
                writer='ffmpeg',
                fps=fps_setting,
                dpi=150,
                progress_callback=lambda i, n: pbar.update(i - pbar.n)
            )
        print("🎬 MP4 saved successfully.")

        if in_jupyter:
            display(HTML(
                f'<video controls autoplay loop>'
                f'<source src="{output_name}.mp4" type="video/mp4">'
                f'</video>'
            ))

    except Exception as e:
        print(f"MP4 Error: {e}")

else:
    print("⚠ MP4 export skipped (ffmpeg not installed).")


try:
    print(f"🖼️ Starting GIF Hunt... (Seed: {seed})")
    with tqdm(total=total_frames, desc="GIF Encoding") as pbar:
        ani.save(
            f"{output_name}.gif",
            writer='pillow',
            fps=fps_setting,
            dpi=100,
            progress_callback=lambda i, n: pbar.update(i - pbar.n)
        )
    print("✨ Hunt Complete! Saved GIF.")

except Exception as e:
    print(f"GIF Error: {e}")

plt.close(fig)
