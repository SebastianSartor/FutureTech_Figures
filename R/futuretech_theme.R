# FutureTech chart palette + ggplot2 theme (R).
# MIRROR of python/futuretech_palette.py and futuretech.mplstyle — keep hex
# values and ordering in sync across both languages.
#
# Usage:
#   source("futuretech_theme.R")
#   ggplot(df, aes(x, y, color = series)) +
#     geom_line(linewidth = 1) +
#     scale_color_futuretech() +
#     theme_futuretech() +
#     ft_direct_labels(df, x, y, series)   # right-side labels, Neil's preference

library(ggplot2)

# ---- MIT FutureTech brand, canonical categorical ordering -------------------
#      (matches CATEGORICAL in Python: blue, MIT red, green, purple, orange ...)
ft_categorical <- c(
  "#1966FF",  # blue
  "#750014",  # MIT red
  "#00AD00",  # green
  "#9933FF",  # purple
  "#ED7700",  # orange (Sloan tertiary)
  "#FF14F0",  # pink
  "#288DC0",  # light blue 2 (Sloan tertiary)
  "#000000"   # black (reserve for emphasis / single series)
)
ft_primary <- "#002896"   # dark blue — single-series / emphasis default
ft_gray    <- list(axis = "#40464C", grid = "#DDE1E6", muted = "#8B959E")

# Sequential (MIT blue family) and diverging (blue <-> red) ramps.
ft_sequential <- c("#99EBFF", "#1966FF", "#002896")
ft_diverging  <- c("#002896", "#1966FF", "#F2F4F8", "#FF1423", "#750014")

scale_color_futuretech <- function(...) {
  scale_color_manual(values = ft_categorical, ...)
}
scale_fill_futuretech <- function(...) {
  scale_fill_manual(values = ft_categorical, ...)
}

# ---- theme: sans, despined, light horizontal grid ---------------------------
theme_futuretech <- function(base_size = 11) {
  theme_minimal(base_size = base_size, base_family = "sans") +
    theme(
      plot.title       = element_text(face = "bold", size = base_size + 3,
                                       color = "#212326", margin = margin(b = 10)),
      axis.title       = element_text(color = ft_gray$axis, size = base_size + 1),
      axis.text        = element_text(color = ft_gray$axis, size = base_size - 1),
      axis.line.x      = element_line(color = ft_gray$axis, linewidth = 0.5),
      axis.line.y      = element_line(color = ft_gray$axis, linewidth = 0.5),
      panel.grid.major.y = element_line(color = ft_gray$grid, linewidth = 0.4),
      panel.grid.major.x = element_blank(),
      panel.grid.minor   = element_blank(),
      legend.position    = "none",   # direct labels are the default
      plot.margin        = margin(10, 60, 10, 10)  # right room for labels
    )
}

# ---- Direct right-side line labels (Neil's preference) -----------------------
# df: data frame; x,y,group are bare column names (tidy-eval).
# Adds geom_text at each line's max-x endpoint, colored by group, clip off.
ft_direct_labels <- function(df, x, y, group, size = 4, hjust = -0.1) {
  x <- rlang::ensym(x); y <- rlang::ensym(y); group <- rlang::ensym(group)
  ends <- do.call(rbind, lapply(split(df, df[[rlang::as_string(group)]]), function(d) {
    d[which.max(d[[rlang::as_string(x)]]), , drop = FALSE]
  }))
  list(
    geom_text(data = ends,
              aes(label = !!group, color = !!group),
              hjust = hjust, fontface = "bold", size = size),
    coord_cartesian(clip = "off")
  )
}