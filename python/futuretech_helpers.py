"""
FutureTech chart helpers (matplotlib).

The headline function is `label_lines`, which places colored text labels near
each line inside the plot (Neil's preference). For crowded graphs, use
mode="right" to place labels in the right margin instead.

Typical use:
    import matplotlib.pyplot as plt
    from futuretech_helpers import use_style, label_lines, save_figure

    use_style()
    fig, ax = plt.subplots()
    for name, y in series.items():
        ax.plot(x, y, label=name)
    label_lines(ax)                         # inline labels near each curve
    # label_lines(ax, mode="right")         # right-margin labels for crowded graphs
    # label_lines(ax, positions={"GDP": (2024, 5.2)})  # manual position override
    ax.set_ylabel("AI Adoption Rate (%)")
    add_logo(fig)                           # FutureTech watermark, bottom-right
    save_figure(fig, "adoption")            # writes adoption.png + adoption.pdf at 300dpi
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

_STYLE = os.path.join(os.path.dirname(__file__), "futuretech.mplstyle")
_LOGO  = os.path.join(os.path.dirname(__file__), "..", "logo-p-1600.png")


def use_style():
    """Apply the FutureTech matplotlib style. Call once before plotting."""
    plt.style.use(_STYLE)


def label_lines(ax, labels=None, positions=None, mode="inline",
                fontsize=13, fontweight="bold",
                x_offset_frac=0.01, x_right_frac=1.02, min_gap_frac=0.045):
    """
    Label plotted lines with colored text — no separate legend box.

    mode="inline" (default): labels appear inside the plot near each line's
        right end, at the line's own y value. Pass `positions` to override
        the placement of any individual line.
    mode="right": labels appear in the right margin outside the plot, y-aligned
        to the line's endpoint. Better when lines crowd the right edge.

    positions : dict {line_label: (x, y)} in data coordinates (inline mode only).
                Unspecified lines are auto-positioned at their last data point.
    labels    : dict {line_label: display_text} to override the displayed string.
    x_offset_frac : tiny rightward nudge from the last point (as a fraction of
                    x-axis span), so the label doesn't sit on the marker.
    min_gap_frac  : minimum vertical spacing between labels in axes-fraction units
                    (collision avoidance).
    """
    lines = [ln for ln in ax.get_lines()
             if ln.get_label() and not ln.get_label().startswith("_")]
    if not lines:
        return

    positions = positions or {}
    label_overrides = labels or {}

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    x_span = xmax - xmin if xmax != xmin else 1.0
    y_span = ymax - ymin if ymax != ymin else 1.0
    _log_y = ax.get_yscale() == "log"

    def _y_frac(y_val):
        """Axes-fraction for y_val, correct on both linear and log scales."""
        try:
            if _log_y:
                import math
                ly = math.log10(max(y_val, 1e-300))
                lymin = math.log10(max(ymin, 1e-300))
                lymax = math.log10(max(ymax, 1e-300))
                span = lymax - lymin if lymax != lymin else 1.0
                return (ly - lymin) / span
            else:
                return (y_val - ymin) / y_span
        except (ValueError, ZeroDivisionError):
            return 0.5

    if mode == "inline":
        entries = []
        for ln in lines:
            xdata, ydata = ln.get_xdata(), ln.get_ydata()
            if len(xdata) == 0:
                continue
            key = ln.get_label()
            text = label_overrides.get(key, key)
            color = ln.get_color()
            if key in positions:
                x_pos, y_pos = positions[key]
            else:
                x_pos = float(xdata[-1]) + x_offset_frac * x_span
                y_pos = float(ydata[-1])
            entries.append([_y_frac(y_pos), x_pos, y_pos, text, color])

        # Collision avoidance: sort by y, nudge overlapping labels upward.
        entries.sort(key=lambda e: e[0])
        for i in range(1, len(entries)):
            if entries[i][0] - entries[i - 1][0] < min_gap_frac:
                entries[i][0] = entries[i - 1][0] + min_gap_frac
                # convert fraction back to data coords for text placement
                if _log_y:
                    import math
                    lymin = math.log10(max(ymin, 1e-300))
                    lymax = math.log10(max(ymax, 1e-300))
                    entries[i][2] = 10 ** (lymin + entries[i][0] * (lymax - lymin))
                else:
                    entries[i][2] = entries[i][0] * y_span + ymin

        for y_frac, x_pos, y_pos, text, color in entries:
            ax.text(x_pos, y_pos, text, va="center", ha="left",
                    fontsize=fontsize, fontweight=fontweight, color=color,
                    clip_on=False, parse_math=False)

    else:  # mode == "right"
        entries = []
        for ln in lines:
            ydata = ln.get_ydata()
            if len(ydata) == 0:
                continue
            key = ln.get_label()
            text = label_overrides.get(key, key)
            y_end = float(ydata[-1])
            entries.append([_y_frac(y_end), text, ln.get_color()])

        entries.sort(key=lambda e: e[0])
        for i in range(1, len(entries)):
            if entries[i][0] - entries[i - 1][0] < min_gap_frac:
                entries[i][0] = entries[i - 1][0] + min_gap_frac

        for y_frac, text, color in entries:
            ax.annotate(text, xy=(x_right_frac, y_frac), xycoords="axes fraction",
                        va="center", ha="left", fontsize=fontsize,
                        fontweight=fontweight, color=color,
                        annotation_clip=False, parse_math=False)

        ax.figure.subplots_adjust(right=0.82)

    leg = ax.get_legend()
    if leg is not None:
        leg.remove()


def direct_label_lines(ax, labels=None, x_frac=1.02, fontsize=13,
                       fontweight="bold", min_gap_frac=0.045):
    """Backwards-compatible alias. Equivalent to label_lines(ax, mode='right')."""
    label_lines(ax, labels=labels, mode="right", fontsize=fontsize,
                fontweight=fontweight, x_right_frac=x_frac,
                min_gap_frac=min_gap_frac)


def add_logo(fig, alpha=0.35, height_frac=0.10, margin_frac=0.01):
    """
    Add the FutureTech logo as a semi-transparent watermark in the bottom-right
    corner of the figure. Call after all subplots are added.

    alpha       : transparency of the logo (0 = invisible, 1 = opaque).
    height_frac : logo height as a fraction of the figure height.
    margin_frac : gap from the figure edges, in figure-fraction units.
    """
    if not os.path.exists(_LOGO):
        return
    try:
        import matplotlib.image as mpimg
        logo = mpimg.imread(_LOGO)
        h, w = logo.shape[:2]
        aspect = w / h
        logo_h = height_frac
        logo_w = height_frac * aspect

        # Build RGBA array with desired alpha.
        if logo.dtype == np.uint8:
            logo = logo.astype(float) / 255.0
        if logo.ndim == 3 and logo.shape[2] == 4:
            rgba = logo.copy()
            rgba[..., 3] *= alpha
        else:
            rgba = np.dstack([logo[..., :3],
                              np.full(logo.shape[:2], alpha, dtype=float)])

        ax_logo = fig.add_axes(
            [1.0 - logo_w - margin_frac, margin_frac, logo_w, logo_h]
        )
        ax_logo.imshow(rgba, aspect="auto", interpolation="lanczos")
        ax_logo.axis("off")
        ax_logo.patch.set_alpha(0)
    except Exception:
        pass  # never break figure rendering for a watermark


def unit_formatter(scale=1, unit="", fmt="{:.3g}"):
    """
    Return a matplotlib FuncFormatter that displays tick values in natural units.

    Examples:
        ax.yaxis.set_major_formatter(unit_formatter(1e6, "M$"))
            # 4000000 → "4 M$"
        ax.xaxis.set_major_formatter(unit_formatter(1e9, "B"))
            # 3500000000 → "3.5 B"
        ax.xaxis.set_major_formatter(unit_formatter(1, "", fmt="{:.0f}"))
            # use when x data is already in natural units (e.g. calendar years)
    """
    def _fmt(x, pos):
        val = x / scale
        s = fmt.format(val)
        return f"{s} {unit}".strip() if unit else s
    return ticker.FuncFormatter(_fmt)


def sync_axes(*axes_list, which="both"):
    """
    Enforce identical axis limits across a list of Axes (for subplot consistency).

    Call after all data is plotted. which: 'x', 'y', or 'both'.

    Example:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        # ... plot on both ...
        sync_axes(ax1, ax2, which="y")   # same y limits on both panels
    """
    if which in ("x", "both"):
        xlims = [ax.get_xlim() for ax in axes_list]
        lo, hi = min(l[0] for l in xlims), max(l[1] for l in xlims)
        for ax in axes_list:
            ax.set_xlim(lo, hi)
    if which in ("y", "both"):
        ylims = [ax.get_ylim() for ax in axes_list]
        lo, hi = min(l[0] for l in ylims), max(l[1] for l in ylims)
        for ax in axes_list:
            ax.set_ylim(lo, hi)


def add_source_note(fig, text, fontsize=9, color="#888888"):
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
