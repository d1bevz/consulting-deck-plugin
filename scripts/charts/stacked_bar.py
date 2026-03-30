"""Stacked Bar Chart — Share-of-X Analysis.

Compares composition/structure across multiple objects.
Examples: budget allocation by department, time distribution, revenue mix.
"""

import plotly.graph_objects as go

from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "categories": ["Product A", "Product B", "Product C"],
    "segments": ["Engineering", "Marketing", "Sales", "Support", "Operations"],
    "values": [
        [35, 25, 30],
        [20, 35, 15],
        [15, 20, 25],
        [20, 10, 20],
        [10, 10, 10],
    ],
    "title": "Engineering dominates Product A spend, while Product B is marketing-heavy",
    "source": "Internal budget data; FY2026 Q1",
}


def create_stacked_bar(
    data: dict,
    title: str | None = None,
    theme_path: str | None = None,
    output_path: str | None = None,
) -> go.Figure:
    """Create a 100% stacked bar chart."""
    theme = load_theme(theme_path)
    palette = theme["colors"]["chart_palette"]

    categories = data["categories"]
    segments = data["segments"]
    values = data["values"]

    totals = [sum(values[s][c] for s in range(len(segments))) for c in range(len(categories))]
    norm_values = [
        [values[s][c] / totals[c] * 100 if totals[c] > 0 else 0 for c in range(len(categories))]
        for s in range(len(segments))
    ]

    fig = go.Figure()

    for i, segment in enumerate(segments):
        fig.add_trace(go.Bar(
            name=segment,
            x=categories,
            y=norm_values[i],
            marker_color=palette[i % len(palette)],
            text=[f"{v:.0f}%" for v in norm_values[i]],
            textposition="inside",
            textfont={"size": 18, "color": "white", "family": "Inter Bold"},
        ))

    layout = get_plotly_layout(
        theme,
        title=title or data.get("title", ""),
        source=data.get("source", ""),
    )
    layout["barmode"] = "stack"
    layout["yaxis"] = {"title": "Share (%)", "range": [0, 100], "showgrid": True,
                        "gridcolor": "#f0f0f0", "title_font": {"size": 16}, "tickfont": {"size": 14}}
    layout["xaxis"] = {"title": "", "tickfont": {"size": 16}}
    layout["legend"] = {"orientation": "h", "y": -0.12, "x": 0.5, "xanchor": "center",
                         "font": {"size": 14}}

    fig.update_layout(**layout)

    if output_path:
        save_chart(fig, output_path)

    return fig


if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data:
        data = DEMO_DATA
    create_stacked_bar(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
