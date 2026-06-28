"""
Reference example: stacked bars with direct in-bar labels.
Shaped like the 'automation by deployment scale' figure.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))
import numpy as np
import matplotlib.pyplot as plt
from futuretech_palette import CATEGORICAL, GRAY
from futuretech_helpers import use_style, save_figure, add_logo

use_style()

cats = ["Individual\nBusinesses", "Industry\nGroups", "Subsectors",
        "Sectors", "U.S.\nEconomy"]
full    = np.array([2, 77, 82, 88, 96])
partial = np.array([8, 20, 16, 11, 4])
none    = 100 - full - partial

colors = [CATEGORICAL[1], CATEGORICAL[0], GRAY["light"]]  # MIT red, blue, light gray

fig, ax = plt.subplots(figsize=(7.5, 5))
x = np.arange(len(cats))
b1 = ax.bar(x, full, color=colors[0], label="Full Automation", width=0.62)
b2 = ax.bar(x, partial, bottom=full, color=colors[1], label="Partial Automation", width=0.62)
b3 = ax.bar(x, none, bottom=full + partial, color=colors[2], label="No Automation", width=0.62)

# In-bar labels for the meaningful segments
for xi, f, p in zip(x, full, partial):
    if f >= 5:
        ax.text(xi, f / 2, f"{f}%", ha="center", va="center", fontsize=9, fontweight="bold")
    if p >= 5:
        ax.text(xi, f + p / 2, f"{p}%", ha="center", va="center", fontsize=9, fontweight="bold")

ax.set_ylabel("Fraction of compensation tasks")
ax.set_xlabel("Deployment Scale")
ax.set_xticks(x); ax.set_xticklabels(cats)
ax.set_ylim(0, 100)
ax.set_yticks(range(0, 101, 20))
ax.set_yticklabels([f"{v}%" for v in range(0, 101, 20)])
ax.grid(axis="x", visible=False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=3, frameon=False)

add_logo(fig)
save_figure(fig, "grouped_bars",
            outdir=os.path.join(os.path.dirname(__file__), "reference_renders"))
print("done")