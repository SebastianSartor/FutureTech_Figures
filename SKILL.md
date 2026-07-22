---
name: futuretech-charts
description: Apply the MIT FutureTech lab house style to any chart, figure, plot, or data visualization, in Python (matplotlib) or R (ggplot2). Use this whenever creating, restyling, or reviewing a figure for a FutureTech paper, slide, or report — even if the user just says "make a chart", "plot this", "visualize", or shares data to graph. Enforces the lab defaults — sans-serif typography, the MIT FutureTech brand palette in a fixed order, despined axes, light horizontal gridlines, and inline line labels (near the curve, inside the plot) instead of legends. Always consult this skill before producing a figure so all lab outputs look consistent.
---

# FutureTech Charts

The MIT FutureTech house style for figures. The goal is that any chart produced
by anyone in the lab is immediately recognizable as ours and looks
publication-ready without per-figure fiddling.

## The non-negotiable defaults

1. **Typography: sans-serif throughout.** Single font family (Source Sans Pro,
   falling back to Helvetica/Arial on machines without it). Titles bold, axis
   labels regular. No serif/LaTeX fonts.

2. **Text sizes: large enough to read on a slide.** Hierarchy (largest → smallest):
   - Slide/deck header (`add_slide_header`): **20 pt bold** — the headline above
     the chart on a slide. This is the largest text on the figure.
   - Figure title (`set_title` / `suptitle`): **17 pt bold**
   - Axis labels: **14 pt regular** (not bold — these are axis descriptors, not
     headers)
   - Tick labels: **12 pt**
   - Direct line labels: **13 pt bold** (same as `label_lines` default)
   Always use the stylesheet sizes — do not override to smaller.

3. **No diagonal tick labels — ever.** Always horizontal. The stylesheet
   enforces `xtick.labelrotation: 0`. If a long category name forces you to
   rotate, abbreviate the label or rotate the whole plot to horizontal bars.

4. **Natural units on axes.** Labels must make sense standalone — a reader
   should not have to read the axis title to decode the scale.
   - Bad: axis shows `4`, title says "Millions of dollars"
   - Good: axis shows `4 M$` or `$4m`, or the data is transformed and the
     axis title says "dollars" with ticks showing `4,000,000`
   - Use `unit_formatter(scale, unit)` to apply this automatically.
   - When the raw data is "years since 2020", transform to actual calendar
     years before plotting so the x axis reads `2020`, `2022`, `2024`.

5. **Color: the MIT FutureTech brand palette, in canonical order.** Series
   index N → color N, always. Never assign colors ad hoc. Pull from
   `CATEGORICAL` in `futuretech_palette.py` (Python) or `ft_categorical` (R).
   - Single-series / emphasis: `PRIMARY` (`#002896` dark blue).
   - Color note: the palette has two reds (MIT red `#750014` at index 1 and
     bright red elsewhere). They can be hard to distinguish in print. If a plot
     has one series that looks "dark red" and another that looks "bright red",
     consider swapping one for a non-red color or faceting.
   - **Consistent across figures:** if the same object (country, model,
     scenario) appears in multiple plots in a paper or slide deck, it must get
     the same color in every plot. Before coding colors, agree on the mapping
     and apply it explicitly (don't rely on automatic cycling across separate
     scripts).

6. **Inline labels instead of legends.** For any plot with ≤ ~6 labeled lines:
   - **Default (`mode="inline"`):** place each colored label inside the plot
     area, near the right end of its line, at the line's own y value. Adjust
     placement per-label via the `positions` dict.
   - **Crowded fallback (`mode="right"`):** labels in the right margin, y
     position aligned to the line's endpoint. Use when lines bunch at the right
     edge and inline labels would overlap each other or the data.
   - **Legend only** when direct labeling is truly infeasible (stacked bars,
     many overlapping categories, etc.). Even then, place it inside the plot.
   Labels are always color-matched to their line.

7. **Despined axes:** drop top and right spines. Light *horizontal* gridlines
   only; no vertical grid on time series.

8. **Non-linear scales must be immediately obvious.** If an axis is log or
   otherwise non-linear:
   - Use decade tick marks labeled as `10¹⁸`, `10¹⁹`, etc. (not `1e18`).
   - Call `ax.set_xscale("log")` / `ax.set_yscale("log")` — do not take the
     log of the data manually and plot it on a linear axis.
   - Add an "axis label (log scale)" suffix or an annotation in-plot if there
     is any chance a reader might miss it.

9. **Consistent axes across subplots / versions.** When a paper or slide deck
   has multiple versions of the same plot (e.g. one curve added per slide),
   the axis limits must be identical across all versions. Use `sharex`/`sharey`
   when building subplots, or call `sync_axes(ax1, ax2, ...)` after plotting.
   Never let matplotlib rescale axes between subplot panels.

10. **FutureTech logo.** Call `add_logo(fig)` before saving. By default the full
    brand logo (grey "MIT", red "FutureTech", tagline) sits **solid** in a
    **footer strip below the plot** — no overlap with data, and not a faded or
    recolored watermark. It is composited onto the white background so its edges
    stay clean. Use `placement="overlay"` only when you explicitly want the
    legacy bottom-right corner mark.

11. **No caption or description under the chart unless explicitly asked.** The
    figure must stand on its own through its title, axis labels, and direct
    labels. Do **not** add an explanatory sentence, interpretation, takeaway, or
    "note:" line beneath (or inside) the chart on your own initiative — resist
    the urge even when the finding feels worth spelling out. Captions belong in
    the surrounding paper/slide text, written by the author. Only add one when
    the user explicitly asks. (`add_source_note()` is the sole exception: a short
    data-source/credit line when a source genuinely needs attributing — never a
    place for commentary or takeaways.)

12. **Save both PNG (300 dpi) and PDF (vector).** `save_figure()` does this.

## How to use it — Python (matplotlib)

This is the primary path. Files live in `python/`.

```python
import sys; sys.path.insert(0, "<skill>/python")
from futuretech_helpers import (
    use_style, label_lines, sync_axes, unit_formatter,
    add_slide_header, add_logo, save_figure
)
from futuretech_palette import categorical, PRIMARY

use_style()                       # applies futuretech.mplstyle

fig, ax = plt.subplots()
add_slide_header(fig, "Labor market effects by sector")  # optional slide headline
for name, y in series.items():
    ax.plot(x, y, label=name)

# Inline labels near each curve (default):
label_lines(ax)

# Override position for one label that would otherwise overlap:
label_lines(ax, positions={"Series A": (2026, 5.2)})

# For a crowded graph — labels in the right margin:
label_lines(ax, mode="right")

ax.set_ylabel("Spending (2023 $)")
ax.yaxis.set_major_formatter(unit_formatter(1e9, "B$"))  # e.g. 4000000000 → "4 B$"

add_logo(fig)                     # FutureTech wordmark in footer strip
save_figure(fig, "myfigure")      # -> myfigure.png + myfigure.pdf
```

Key functions (see `python/futuretech_helpers.py` for full signatures):
- `use_style()` — apply the stylesheet. Call once before plotting.
- `label_lines(ax, labels=None, positions=None, mode="inline", ...)` — the
  headline feature. Places colored labels near each line (inline or right-side),
  collision-avoids overlaps, removes any legend.
- `direct_label_lines(ax, ...)` — legacy alias for `mode="right"`.
- `unit_formatter(scale, unit, fmt)` — returns a `FuncFormatter` for natural
  unit tick labels. Pass to `ax.yaxis.set_major_formatter(...)`.
- `add_slide_header(fig, text, fontsize=20)` — large bold slide headline above
  the plot (larger than the figure title).
- `sync_axes(*axes, which="both")` — equalize limits across subplot panels.
- `add_logo(fig, placement="footer")` — full brand logo, solid, in a footer
  strip below the plot (default). `placement="overlay"` for the corner mark.
- `add_source_note(fig, text)` — small italic data-source/credit line,
  bottom-left. Not for commentary or takeaways (see rule 11).
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
  ft_label_lines(df, x, y, series)          # inline labels (default)
  # ft_label_lines(df, x, y, series, mode="right")  # right-margin fallback
```

## Capitalization rules

Apply these consistently so all lab figures look like they came from the same
pen:

- **Figure titles**: sentence case — capitalize only the first word and proper
  nouns (country names, model names, "AI", "GDP", etc.).
  - "Labor market effects by sector" ✓ — "Labor Market Effects By Sector" ✗
- **Axis labels**: sentence case, same rule.
  - "Real wage growth (%)" ✓ — "Real Wage Growth (%)" ✗
- **Inline line / bar labels**: match the capitalization used for that entity
  everywhere else in the paper/slides (usually title case for named entities:
  "United States", "GPT-4").
- **Tick labels**: never title-case. Numbers and units only (e.g. `"4 M$"`).

## Choosing the right chart

- **Time series / trends** → line plot, inline labels.
- **Composition across a few categories** → stacked bars with in-bar % labels
  and an inside-plot legend only if necessary.
- **Scaling / log relationships** (FLOPs, params) → scatter + fit line, log
  axes, annotate the fit (coefficient / R²) in-plot rather than in a caption.
- **> 6 series** → don't crowd inline labels; facet, or group categories first.

## Making progressive slide versions

When the user asks for **multiple versions of a plot with elements added
progressively** (one per slide):

1. **Ask the user** what order the elements should appear. Do not guess.
2. Build a factory function that accepts a subset of series/elements and
   returns a fully styled figure.
3. For each prefix of the ordered list, call the factory and save a numbered
   output (`myfig_v1.png`, `myfig_v2.png`, ...).
4. Use `sync_axes()` across all versions so axes never jump between slides.
5. Keep labels consistent — a label present in slide N must appear in exactly
   the same position in slide N+1 (only new labels appear newly).

## Edge cases & rules of thumb

- **Dollar signs / special chars in labels**: the helper renders text literally
  (`parse_math=False`), so `$1m-$10m` displays correctly. In raw matplotlib
  calls, pass `parse_math=False` or escape `\$`.
- **Log scales**: keep the despined look; label decade ticks (10¹⁸, 10¹⁹ …).
- **Percent axes**: format ticks as `"{v}%"` via `unit_formatter(1, "%", "{:.0f}")`,
  don't rely on a `%` axis label alone.
- **Color count**: the categorical palette holds ~5 well-separated hues; black
  (index 7) is reserved for emphasis or a single-series plot. Bright fills
  (pink, light green, yellow) are fine for bar fills but low-contrast for thin
  lines — avoid them there.
- **Accessibility**: the brand palette is not strictly colorblind-safe, so color
  is never the only channel — we label lines directly (the default) and, for
  >4 lines, also vary marker shape or facet.

## When to consult the reference renders

Before finalizing a figure, compare against the PNGs in
`examples/reference_renders/`. They are the calibration target for "what good
looks like." The matching scripts in `examples/` show exactly how they were
made.

## Updating this skill

The lab style evolves as Neil gives feedback and as people hit uncovered cases.
To change it: edit the files here, re-render the example PNGs so they reflect
the new look, re-package the `.skill`, and re-upload it to the lab's Claude
workspace.

The cardinal rule: **palette hex values and ordering must stay identical between
`python/futuretech_palette.py` and `R/futuretech_theme.R`** — they are one
source of truth in two languages. If you touch one, touch the other in the same
edit.

Anything that changes a default everyone sees (palette, fonts, label placement)
is Neil's call and should get his sign-off first. Adding a new chart-type
example to `examples/` does not.
