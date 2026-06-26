---
name: futuretech-charts
description: Apply the MIT FutureTech lab house style to any chart, figure, plot, or data visualization, in Python (matplotlib) or R (ggplot2). Use this whenever creating, restyling, or reviewing a figure for a FutureTech paper, slide, or report — even if the user just says "make a chart", "plot this", "visualize", or shares data to graph. Enforces the lab defaults — sans-serif typography, the MIT FutureTech brand palette in a fixed order, despined axes, light horizontal gridlines, and direct right-side line labels instead of legends (advisor Neil Thompson's stated preference). Always consult this skill before producing a figure so all lab outputs look consistent.
---

# FutureTech Charts

The MIT FutureTech house style for figures. The goal is that any chart produced
by anyone in the lab is immediately recognizable as ours and looks
publication-ready without per-figure fiddling.

## The non-negotiable defaults

1. **Typography: sans-serif throughout.** Titles bold, axis labels regular. No
   serif/LaTeX fonts. (Font fallback chain handles machines without installs.)
2. **Color: the MIT FutureTech brand palette, in the canonical order**
   defined in the palette files (blue → MIT red → green → purple → orange …).
   Series index N → color N, always. Never assign colors ad hoc — pull them in
   order so the same series gets the same color across every figure in a paper.
   Single-series / emphasis plots use the dark-blue PRIMARY.
3. **Direct right-side labels, not legends** (Neil's preference): for any plot
   with roughly ≤6 labeled lines/series, place a colored label to the right of
   the plot next to where each line ends. Use a legend ONLY when direct labeling
   is infeasible (e.g. stacked bars, many overlapping categories).
4. **Despined axes**: drop the top and right spines. Light *horizontal*
   gridlines only; no vertical grid on time series.
5. **Save both PNG (300 dpi, for slides/docs) and PDF (vector, for papers).**

## How to use it — Python (matplotlib)

This is the primary path. Files live in `python/`.

```python
import sys; sys.path.insert(0, "<skill>/python")
from futuretech_helpers import use_style, direct_label_lines, save_figure
from futuretech_palette import categorical, PRIMARY  # if you need explicit colors

use_style()                       # applies futuretech.mplstyle (fonts, palette, despine)
fig, ax = plt.subplots()
for name, y in series.items():
    ax.plot(x, y, label=name)     # colors auto-cycle in canonical order
direct_label_lines(ax)            # right-side labels; removes the legend for you
ax.set_ylabel("…")
save_figure(fig, "myfigure")      # -> myfigure.png + myfigure.pdf
```

Key functions (see `python/futuretech_helpers.py` for full signatures):
- `use_style()` — apply the stylesheet. Call once before plotting.
- `direct_label_lines(ax, labels=None, ...)` — the headline feature. Places
  colored labels right of the plot, collision-avoids overlaps, strips the legend.
- `add_source_note(fig, text)` — small italic credit line bottom-left.
- `save_figure(fig, name, outdir=".")` — writes PNG + PDF at publication DPI.

Palette: `python/futuretech_palette.py` exposes `CATEGORICAL` (ordered list),
`categorical(n)`, `PRIMARY`, `MIT_CORE` / `BRAND` / `TERTIARY` (named dicts),
plus `SEQUENTIAL` and `DIVERGING` ramps for ordered/signed data.

## How to use it — R (ggplot2)

Parity path. File: `R/futuretech_theme.R`. Hex values mirror the Python source.

```r
source("<skill>/R/futuretech_theme.R")
ggplot(df, aes(x, y, color = series)) +
  geom_line(linewidth = 1) +
  scale_color_futuretech() +
  theme_futuretech() +
  ft_direct_labels(df, x, y, series)   # right-side labels
```

## Choosing the right chart

- **Time series / trends** → line plot, direct right labels. (Reference:
  `examples/reference_renders/timeseries_direct_labels.png`)
- **Composition across a few categories** → stacked bars with in-bar % labels
  and a top legend. (Reference: `examples/reference_renders/grouped_bars.png`)
- **Scaling / log relationships** (FLOPs, params) → scatter + fit line, log axes,
  annotate the fit (coefficient / R²) in-plot rather than in a caption.
- **>6 series** → don't crowd direct labels; facet, or group categories first.

## Edge cases & rules of thumb

- **Dollar signs / special chars in labels**: the helper renders text literally
  (mathtext disabled), so `$1m-$10m` displays correctly. In raw matplotlib calls,
  pass `parse_math=False` or escape `\$`.
- **Log scales**: keep the despined look; label decade ticks (10¹⁸, 10¹⁹ …).
- **Percent axes**: format ticks as `"{v}%"`, don't rely on a `%` axis label alone.
- **Color count**: the categorical palette holds ~5 well-separated hues; black
  (index 7) is reserved for emphasis or a single-series plot. Bright fills
  (pink, light green, yellow) are fine for bar fills but low-contrast for thin
  lines — avoid them there.
- **Accessibility**: the brand palette is not strictly colorblind-safe, so color
  is never the only channel — we label lines directly (the default) and, for >4
  lines, also vary marker shape or facet. For figures where colorblind-safety is
  a hard requirement, fall back to a sequential single-hue encoding.

## When to consult the reference renders

Before finalizing a figure, compare against the PNGs in
`examples/reference_renders/`. They are the calibration target for "what good
looks like." The matching scripts in `examples/` show exactly how they were made.

## Updating this skill

The lab style evolves as Neil gives feedback and as people hit uncovered cases.
To change it: edit the files here, re-render the example PNGs so they reflect the
new look, re-package the `.skill`, and re-upload it to the lab's Claude workspace.

The cardinal rule: **palette hex values and ordering must stay identical between
`python/futuretech_palette.py` and `R/futuretech_theme.R`** — they are one source
of truth in two languages. If you touch one, touch the other in the same edit.

Anything that changes a default everyone sees (palette, fonts, label placement)
is Neil's call and should get his sign-off first. Adding a new chart-type example
to `examples/` does not.