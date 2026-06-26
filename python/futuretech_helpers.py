"""
FutureTech chart helpers (matplotlib).

The headline function is `direct_label_lines`, which implements Neil's preference:
labels for each line sit to the RIGHT of the plot, next to the line itself,
colored to match — no legend box. This is the lab default for any plot with
<= ~6 labeled series.

Typical use:
    import matplotlib.pyplot as plt
    from futuretech_helpers import use_style, direct_label_lines, save_figure

    use_style()
    fig, ax = plt.subplots()
    for name, y in series.items():
        ax.plot(x, y, label=name)
    direct_label_lines(ax)          # places right-side labels, removes legend
    ax.set_ylabel("AI Adoption Rate (%)")
    save_figure(fig, "adoption")    # writes adoption.png + adoption.pdf at 300dpi
"""
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager

_STYLE = os.path.join(os.path.dirname(__file__), "futuretech.mplstyle")


def use_style():
    """Apply the FutureTech matplotlib style. Call once before plotting."""
    plt.style.use(_STYLE)


def direct_label_lines(ax, labels=None, x_frac=1.02, fontsize=11,
                       fontweight="bold", min_gap_frac=0.045):
    """
    Place a colored label to the right of each line, vertically aligned to where
    the line ends, instead of a legend. Collision-avoids overlapping labels.

    ax        : the Axes containing Line2D objects (created via ax.plot(..., label=))
    labels    : optional dict {line_label: display_text}; defaults to the line labels
    x_frac    : x position of labels in axes fraction (1.02 = just right of plot)
    min_gap_frac : minimum vertical spacing between labels, in axes-fraction units
    """
    lines = [ln for ln in ax.get_lines() if ln.get_label()
             and not ln.get_label().startswith("_")]
    if not lines:
        return

    # Compute each line's endpoint y in data coords, convert to axes fraction.
    ymin, ymax = ax.get_ylim()
    entries = []
    for ln in lines:
        ydata = ln.get_ydata()
        if len(ydata) == 0:
            continue
        y_end = ydata[-1]
        y_frac = (y_end - ymin) / (ymax - ymin) if ymax != ymin else 0.5
        text = (labels or {}).get(ln.get_label(), ln.get_label())
        entries.append([y_frac, text, ln.get_color()])

    # Collision avoidance: sort by y, nudge apart so labels don't overlap.
    entries.sort(key=lambda e: e[0])
    for i in range(1, len(entries)):
        if entries[i][0] - entries[i - 1][0] < min_gap_frac:
            entries[i][0] = entries[i - 1][0] + min_gap_frac

    for y_frac, text, color in entries:
        ax.annotate(text, xy=(x_frac, y_frac), xycoords="axes fraction",
                    va="center", ha="left", fontsize=fontsize,
                    fontweight=fontweight, color=color, annotation_clip=False,
                    parse_math=False)  # render $ literally, not as LaTeX math

    # Remove any legend; direct labels replace it.
    leg = ax.get_legend()
    if leg is not None:
        leg.remove()

    # Make room on the right for the labels.
    ax.figure.subplots_adjust(right=0.82)


def add_source_note(fig, text, fontsize=8, color="#888888"):
    """Add a small left-aligned source/credit note at the bottom of the figure."""
    fig.text(0.0, -0.02, text, ha="left", va="top",
             fontsize=fontsize, color=color, style="italic")


def save_figure(fig, name, outdir=".", formats=("png", "pdf")):
    """
    Save a figure as both raster (PNG, for slides/docs) and vector (PDF, for papers)
    at publication DPI. Returns the list of written paths.
    """
    os.makedirs(outdir, exist_ok=True)
    paths = []
    for fmt in formats:
        p = os.path.join(outdir, f"{name}.{fmt}")
        fig.savefig(p, format=fmt, bbox_inches="tight")
        paths.append(p)
    return paths