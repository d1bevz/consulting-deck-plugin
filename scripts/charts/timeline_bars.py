"""Timeline Bars — Historical Evolution.

Shows how a metric changed over time with key events.
Like the BCG "Romance" slide: X = time axis (years), Y = intensity,
each bar represents a period/event with label and annotation.

Examples: company growth by funding rounds, product evolution, market entry.
"""

import plotly.graph_objects as go

from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "periods": [
        {"year": "2019", "label": "Idea", "value": 10, "color": "muted", "annotation": "Side project"},
        {"year": "2020", "label": "MVP", "value": 25, "color": "muted", "annotation": ""},
        {"year": "2021", "label": "Pre-seed", "value": 40, "color": "secondary", "annotation": "$500K"},
        {"year": "2022", "label": "Pivot", "value": 15, "color": "danger", "annotation": "Market shift"},
        {"year": "2023", "label": "Seed", "value": 55, "color": "secondary", "annotation": "$2M"},
        {"year": "2024", "label": "PMF", "value": 75, "color": "success", "annotation": "Product-market fit"},
        {"year": "2025", "label": "Series A", "value": 90, "color": "accent", "annotation": "$12M"},
        {"year": "2026", "label": "Now", "value": 95, "color": "primary", "annotation": "Scaling"},
    ],
    "title": "Growth accelerated after pivot, with Series A marking inflection point",
    "source": "Company records; internal analysis",
}


def create_timeline_bars(data, title=None, theme_path=None, output_path=None):
    """Create a timeline bar chart — years on X axis, intensity bars with labels."""
    theme = load_theme(theme_path)
    colors = theme["colors"]
    periods = data["periods"]

    years = [p["year"] for p in periods]
    values = [p["value"] for p in periods]
    labels = [p["label"] for p in periods]
    max_val = max(values)

    bar_colors = []
    for p in periods:
        color_key = p.get("color", "primary")
        bar_colors.append(colors.get(color_key, color_key))

    fig = go.Figure()

    # Main bars — use year strings as categorical x-axis
    fig.add_trace(go.Bar(
        x=years,
        y=values,
        marker_color=bar_colors,
        marker_line={"width": 0},
        width=0.6,
        showlegend=False,
    ))

    # Build annotations: label ON TOP of each bar, annotation ABOVE that
    annotations_list = []
    for i, p in enumerate(periods):
        v = p["value"]

        # Label name above the bar (the main label like "Idea", "MVP", etc.)
        annotations_list.append({
            "x": years[i],
            "y": v,
            "text": f"<b>{labels[i]}</b>",
            "showarrow": False,
            "yshift": 12,
            "font": {"size": 20, "color": colors["text"], "family": "Inter Bold"},
            "xanchor": "center",
            "yanchor": "bottom",
        })

        # Annotation (event details) above the label
        if p.get("annotation"):
            annotations_list.append({
                "x": years[i],
                "y": v,
                "text": p["annotation"],
                "showarrow": False,
                "yshift": 40,
                "font": {"size": 14, "color": colors["muted"]},
                "xanchor": "center",
                "yanchor": "bottom",
            })

    # Timeline arrow at the bottom
    fig.add_annotation(
        x=1, y=-0.08,
        xref="paper", yref="paper",
        text="<b>Time →</b>",
        showarrow=False,
        font={"size": 14, "color": colors["muted"]},
        xanchor="right",
    )

    layout = get_plotly_layout(
        theme,
        title=title or data.get("title", ""),
        source=data.get("source", ""),
    )
    layout["xaxis"] = {
        "title": "",
        "type": "category",
        "tickfont": {"size": 18, "color": colors["text"], "family": "Inter Bold"},
        "showgrid": False,
        "showline": True,
        "linecolor": colors["muted"],
        "linewidth": 2,
    }
    layout["yaxis"] = {
        "title": {"text": "Intensity", "font": {"size": 16}},
        "showgrid": True,
        "gridcolor": "#f0f0f0",
        "range": [0, max_val * 1.45],
        "tickfont": {"size": 14},
    }
    layout["showlegend"] = False
    layout["margin"] = {"l": 80, "r": 60, "t": 120, "b": 100}
    layout["annotations"] = layout.get("annotations", []) + annotations_list

    fig.update_layout(**layout)

    if output_path:
        save_chart(fig, output_path)
    return fig


if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data:
        data = DEMO_DATA
    create_timeline_bars(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
