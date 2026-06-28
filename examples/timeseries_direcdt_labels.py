"""
Reference example: time series with right-side direct labels (Neil's preference).
Reproduces the 'AI Adoption Rate by Wage Spending Groups' figure in house style.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))
import numpy as np
import matplotlib.pyplot as plt
from futuretech_helpers import use_style, direct_label_lines, add_logo, save_figure

use_style()

# Synthetic data shaped like the original (monthly, ~2022-08 to 2025-09).
n = 38
x = np.arange(n)
rng = np.random.default_rng(7)

def ramp(end, curve, jitter):
    base = end * (np.linspace(0, 1, n) ** curve)
    return np.clip(base + rng.normal(0, jitter, n).cumsum() * 0.04, 0, None)

series = {
    ">$10m":      ramp(34, 0.75, 0.6),
    "$1m-$10m":   ramp(17.5, 1.1, 0.3),
    "$100k-$1m":  ramp(10.5, 1.3, 0.2),
    "<$100k":     ramp(5.2, 1.4, 0.15),
}

fig, ax = plt.subplots(figsize=(8, 4.8))
for name, y in series.items():
    ax.plot(x, y, marker="o", markersize=3.5, label=name)

ax.set_ylabel("AI Adoption Rate (%)")
ax.set_title("AI Adoption Rate by 2023 Wage Spending Groups Over Time")
ax.set_ylim(0, 40)

# x tick labels as quarters
ticks = np.arange(1, n, 3)
labels = ["2022-09","2022-12","2023-03","2023-06","2023-09","2023-12",
          "2024-03","2024-06","2024-09","2024-12","2025-03","2025-06","2025-09"]
ax.set_xticks(ticks[:len(labels)])
ax.set_xticklabels(labels, rotation=45, ha="right")

direct_label_lines(ax)
add_logo(fig)

save_figure(fig, "timeseries_direct_labels",
            outdir=os.path.join(os.path.dirname(__file__), "reference_renders"))
print("done")