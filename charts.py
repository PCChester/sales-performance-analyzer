import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path


# ─────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────
PALETTE   = ["#2D6A9F", "#3A9BD5", "#50C4ED", "#72EFDD", "#B9FAD4"]
BG_COLOR  = "#F8F9FB"
GRID_COLOR = "#E2E8F0"
FONT_COLOR = "#1E293B"

plt.rcParams.update({
    "font.family":      "sans-serif",
    "text.color":       FONT_COLOR,
    "axes.labelcolor":  FONT_COLOR,
    "xtick.color":      FONT_COLOR,
    "ytick.color":      FONT_COLOR,
    "axes.spines.top":  False,
    "axes.spines.right": False,
})


def _format_dollars(val, _):
    """Axis tick formatter: $1.2k / $1.2M"""
    if val >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    if val >= 1_000:
        return f"${val/1_000:.0f}k"
    return f"${val:.0f}"


# ─────────────────────────────────────────────
# CHART 1 — Top Categories (horizontal bar)
# ─────────────────────────────────────────────
def chart_top_categories(summary: dict, out_dir: Path):
    data     = summary["top_products"]
    labels   = list(data.keys())
    values   = list(data.values())

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    bars = ax.barh(labels[::-1], values[::-1], color=PALETTE, height=0.55)

    # Value labels on each bar
    for bar, val in zip(bars, values[::-1]):
        ax.text(
            bar.get_width() + max(values) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            _format_dollars(val, None),
            va="center", fontsize=9, color=FONT_COLOR
        )

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_format_dollars))
    ax.set_xlim(0, max(values) * 1.18)
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Revenue by Top Product Category", fontsize=13,
                 fontweight="bold", pad=14, color=FONT_COLOR)
    ax.set_xlabel("Total Revenue", labelpad=8)

    plt.tight_layout()
    path = out_dir / "chart_top_categories.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    print(f"   ✅ Saved {path}")


# ─────────────────────────────────────────────
# CHART 2 — Monthly Revenue Trend (line)
# ─────────────────────────────────────────────
def chart_monthly_trend(summary: dict, out_dir: Path):
    data   = summary["last_6_months"]
    months = list(data.keys())
    values = list(data.values())

    # Flag the last month as partial if it has far less revenue
    avg_full = sum(values[:-1]) / max(len(values) - 1, 1)
    last_is_partial = values[-1] < avg_full * 0.3

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # Solid line for confirmed months, dashed for partial
    solid_x = months[:-1] if last_is_partial else months
    solid_y = values[:-1] if last_is_partial else values

    ax.plot(solid_x, solid_y, color=PALETTE[0], linewidth=2.5,
            marker="o", markersize=7, zorder=3)

    if last_is_partial:
        ax.plot([months[-2], months[-1]], [values[-2], values[-1]],
                color=PALETTE[0], linewidth=2, linestyle="--",
                marker="o", markersize=7, zorder=3)
        ax.annotate("Partial month", xy=(months[-1], values[-1]),
                    xytext=(0, 12), textcoords="offset points",
                    ha="center", fontsize=8, color="#94A3B8")

    # Subtle area fill
    ax.fill_between(months, values, alpha=0.08, color=PALETTE[0])

    # Data labels
    for x, y in zip(months, values):
        ax.annotate(_format_dollars(y, None), (x, y),
                    textcoords="offset points", xytext=(0, 10),
                    ha="center", fontsize=8, color=FONT_COLOR)

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_format_dollars))
    ax.set_ylim(0, max(values) * 1.22)
    ax.grid(axis="y", color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Monthly Revenue Trend (Last 6 Months)", fontsize=13,
                 fontweight="bold", pad=14, color=FONT_COLOR)
    ax.set_xlabel("Month", labelpad=8)
    ax.set_ylabel("Revenue", labelpad=8)

    plt.tight_layout()
    path = out_dir / "chart_monthly_trend.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    print(f"   ✅ Saved {path}")


# ─────────────────────────────────────────────
# CHART 3 — Revenue by Region (donut)
# ─────────────────────────────────────────────
def chart_region_donut(summary: dict, out_dir: Path):
    data   = summary["revenue_by_region"]
    labels = list(data.keys())
    values = list(data.values())
    total  = sum(values)

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    wedges, _ = ax.pie(
        values,
        labels=None,
        colors=PALETTE[:len(labels)],
        startangle=90,
        wedgeprops=dict(width=0.52, edgecolor=BG_COLOR, linewidth=2),
    )

    # Custom legend with value + percentage
    legend_labels = [
        f"{lbl}   {_format_dollars(val, None)}  ({val/total*100:.1f}%)"
        for lbl, val in zip(labels, values)
    ]
    ax.legend(wedges, legend_labels, loc="lower center",
              bbox_to_anchor=(0.5, -0.08), fontsize=9,
              frameon=False, ncol=2)

    # Centre label
    ax.text(0, 0, f"${total/1_000:.0f}k\ntotal",
            ha="center", va="center", fontsize=13,
            fontweight="bold", color=FONT_COLOR)

    ax.set_title("Revenue by Region", fontsize=13,
                 fontweight="bold", pad=14, color=FONT_COLOR)

    plt.tight_layout()
    path = out_dir / "chart_region_donut.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    print(f"   ✅ Saved {path}")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
def generate_charts(summary: dict):
    """Generate all three charts and save to output/."""
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    chart_top_categories(summary, out_dir)
    chart_monthly_trend(summary, out_dir)
    chart_region_donut(summary, out_dir)

    print("📊 All charts saved to output/")


if __name__ == "__main__":
    with open("output/summary.json") as f:
        summary = json.load(f)
    generate_charts(summary)