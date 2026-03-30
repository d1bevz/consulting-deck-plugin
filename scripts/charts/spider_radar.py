"""Spider / Radar Chart — Multi-dimensional Comparison.

Compares 2+ profiles across multiple dimensions.
Examples: competitor analysis, team skills, product feature comparison.
"""

import plotly.graph_objects as go

from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "axes": ["Product Quality", "Price", "UX/Design", "Support", "Performance", "Security", "Integration"],
    "profiles": [
        {"name": "Our Product", "values": [85, 70, 90, 80, 75, 85, 60]},
        {"name": "Competitor X", "values": [80, 85, 65, 70, 90, 80, 85]},
    ],
    "title": "We lead in UX and security; integration and price are the biggest gaps",
    "source": "Product benchmark analysis; March 2026",
}


def _hex_to_rgba(hex_color: str, alpha: float = 0.1) -> str:
    """Convert a hex color string to an rgba() string with given alpha."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def create_spider_radar(
    data: dict,
    title: str | None = None,
    theme_path: str | None = None,
    output_path: str | None = None,
) -> go.Figure:
    """Create a spider/radar chart comparing profiles across dimensions."""
    theme = load_theme(theme_path)
    colors = theme["colors"]
    palette = theme["colors"]["chart_palette"]
    axes = data["axes"]
    profiles = data["profiles"]

    fig = go.Figure()
    for i, profile in enumerate(profiles):
        values = profile["values"] + [profile["values"][0]]
        labels = axes + [axes[0]]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            name=profile["name"],
            line={"color": palette[i % len(palette)], "width": 2.5},
            fill="toself",
            fillcolor=_hex_to_rgba(palette[i % len(palette)], 0.1),
        ))

    layout = get_plotly_layout(
        theme,
        title=title or data.get("title", ""),
        source=data.get("source", ""),
    )
    layout["polar"] = {
        "radialaxis": {"visible": True, "range": [0, 100], "showgrid": True, "gridcolor": "#f0f0f0"},
        "angularaxis": {"gridcolor": "#e0e0e0"},
        "bgcolor": colors["background"],
    }
    layout["legend"] = {"orientation": "h", "y": -0.08, "x": 0.5, "xanchor": "center"}
    fig.update_layout(**layout)

    if output_path:
        save_chart(fig, output_path)

    return fig


if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data:
        data = DEMO_DATA
    create_spider_radar(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
