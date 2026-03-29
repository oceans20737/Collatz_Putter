[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19308908.svg)](https://doi.org/10.5281/zenodo.19308908)
# Base-3 Putter Shot: Friction Dynamics in the Shiftless Collatz Model  
*“Hunting the truth of the Collatz Conjecture on the base-3 Green”*

**Author:** Hiroshi Harada  
**License:** MIT License  
**Date:** March 29, 2026  

---

## Overview
This repository provides a set of Python visualizers (Static & Animated) for exploring the Collatz conjecture through the lens of the **Shiftless model** and **base-3 polar coordinates**.

By interpreting the mathematical transformation as a dynamic **putter shot** on a logarithmic spiral green, we can observe how the Least Significant Bit (LSB) acts as a physical friction coefficient  
$$\mu_k = \frac{\mathrm{LSB}}{B_{k+1}},$$
bending the trajectory step by step until it ultimately falls into a pure power of two ($2^M$).

---

## Key Features
- **Billiard-Style Animation:** Step-by-step dynamic rendering that visually represents the “information collisions” occurring at each state.

- **Overflow Armor:** Safely computes logarithmic values for astronomically large integers without triggering `OverflowError`, enabling the hunt for massive seeds.

- **Scale Locking:** Fixes the polar axis limits in advance, ensuring perfectly stable visuals with zero jitter—even during the final flag deployment.

- **Dual Export:** Built-in support for MP4 (requires `ffmpeg`) and GIF (via Pillow), complete with `tqdm` progress bars.

---

## How to Read the Plot (Visual Guide)
- **The Log-Spiral Green (Background):** A Base-3 polar coordinate system.  
  Radius: logarithmic scale of the integer ($r = \log_3 n$)  
  Angle: base-3 phase ($\theta = 2\pi\{\log_3 n\}$)

- **White Starry Wells:** Perfect powers of two ($2^N$).  
  These represent the potential targets—or “cups”—densely scattered across the green.

- **The Trajectory (Colored Path):** The discrete steps of the Shiftless Collatz sequence.

- **Friction Heatmap ($\mu_k$):** The color and thickness of the path reflect the instantaneous LSB friction coefficient  
  $$\mu_k = \frac{\mathrm{LSB}}{B_{k+1}}.$$

  - **Cyan / Thin lines:** Low friction. Historical momentum dominates, and the sequence moves smoothly along its deterministic inertia.  
  - **Magenta / Thick lines:** High friction. Strong LSB intervention causes chaotic, sharp turns—representing critical “information collisions.”

- **The Yellow Flag & Star:** The final jackpot.  
  The sequence reaches a pure power of two ($2^M$), fully resolving into the target well and ending the shot.

---

## Requirements
Install the required Python packages:

```bash
pip install numpy matplotlib tqdm
```

*(Optional) For high-quality MP4 export, ensure `ffmpeg` is installed on your system.*

---

## Usage
Run the script in your terminal or Jupyter Notebook.  
You can change the starting number by modifying the `seed` variable:

```python
# Change the seed to hunt different trajectories
seed = 27
```

---
