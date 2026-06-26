"""
FutureTech chart palette — the single source of truth for colors.

The lab standard is the **MIT FutureTech brand palette** (MIT core + FutureTech
secondary + selected Sloan tertiary accents). The ORDER below is tuned for
line/series plots: one hue per series, mid-tones, sequenced for adjacent
contrast (blue -> red -> green -> purple -> orange ...). Series index N always
maps to the same color, which is what makes "consistent coloring across figures"
automatic: never assign colors ad hoc, always pull from CATEGORICAL in order.

Because the lab labels lines directly (color is not the only channel that
distinguishes series), the categorical palette prioritizes brand fidelity over
strict colorblind-safety. For >5 series, prefer faceting or grouping rather than
relying on color alone.

Mirror of R/futuretech_theme.R — if you change a hex value, change it in BOTH.
"""

# ---- MIT core palette --------------------------------------------------------
MIT_CORE = {
    "mit_red":      "#750014",
    "silver_gray":  "#8B959E",
    "bright_red":   "#FF1423",
    "black":        "#000000",
    "white":        "#FFFFFF",
}

# ---- FutureTech secondary palette (dark / mid / light per hue) ---------------
BRAND = {
    # pink
    "dark_pink":   "#750062",
    "pink":        "#FF14F0",
    "light_pink":  "#FFB3FF",
    # purple
    "dark_purple": "#3E006B",
    "purple":      "#9933FF",
    "light_purple":"#BFB3FF",
    # blue
    "dark_blue":   "#002896",
    "blue":        "#1966FF",
    "light_blue":  "#99EBFF",
    # green
    "dark_green":  "#004D1A",
    "green":       "#00AD00",
    "light_green": "#AAFF33",
    # yellow
    "yellow":      "#FFEB00",
    # grays
    "dark_gray_1":        "#40464C",
    "dark_gray_2":        "#212326",
    "dark_silver_gray":   "#626A73",
    "light_silver_gray":  "#B8C2CC",
    "light_gray_1":       "#F2F4F8",
    "light_gray_2":       "#DDE1E6",
}

# ---- Tertiary (selected Sloan accents) ---------------------------------------
TERTIARY = {
    "orange":        "#ED7700",
    "light_orange":  "#F6B221",
    "light_blue_2":  "#288DC0",
    "bright_red":    "#EC0044",
}

# Ordered categorical palette for series (line index 0,1,2,... -> these in order)
# One hue per series, mid-tones; sequenced blue -> red -> green -> purple -> orange.
CATEGORICAL = [
    BRAND["blue"],        # 0  #1966FF
    MIT_CORE["mit_red"],  # 1  #750014
    BRAND["green"],       # 2  #00AD00
    BRAND["purple"],      # 3  #9933FF
    TERTIARY["orange"],   # 4  #ED7700
    BRAND["pink"],        # 5  #FF14F0
    TERTIARY["light_blue_2"], # 6  #288DC0
    MIT_CORE["black"],    # 7  #000000  (reserve for emphasis / single series)
]

# Single-series / emphasis color (one-line plots, regression fits, default look).
PRIMARY = BRAND["dark_blue"]   # #002896

# Neutral grays for axes, gridlines, secondary annotation (from brand grays).
GRAY = {
    "axis":   "#40464C",   # dark_gray_1
    "grid":   "#DDE1E6",   # light_gray_2
    "muted":  "#8B959E",   # silver_gray
    "light":  "#F2F4F8",   # light_gray_1
}

# Sequential ramp (ordered categories / heat-like encodings), MIT blue family.
SEQUENTIAL = ["#99EBFF", "#1966FF", "#002896"]   # light_blue -> blue -> dark_blue

# Diverging ramp (signed quantities), blue <-> red through neutral.
DIVERGING = ["#002896", "#1966FF", "#F2F4F8", "#FF1423", "#750014"]


def categorical(n):
    """Return the first n series colors in canonical order."""
    if n > len(CATEGORICAL):
        raise ValueError(
            f"{n} series requested but palette defines {len(CATEGORICAL)}. "
            "For >8 series, reconsider the encoding (facet, or group categories)."
        )
    return CATEGORICAL[:n]