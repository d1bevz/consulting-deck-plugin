"""Timeline Bars — Historical Evolution.

Shows how a metric changed over time with events of varying duration and intensity.
Inspired by BCG "Romance" slide: X = continuous time axis, Y = intensity,
bar WIDTH = duration of event, bar POSITION = when it occurred.

This is NOT a categorical bar chart — it's a timeline with rectangles.

Examples: company growth by funding rounds, product evolution, market entry,
relationship/project history with varying durations.
"""

import plotly.graph_objects as go

from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "periods": [
        {"start": 2018.0, "end": 2019.0, "label": "Idea", "value": 15, "color": "muted", "annotation": "Side project"},
        {"start": 2019.0, "end": 2019.8, "label": "MVP", "value": 30, "color": "muted", "annotation": ""},
        {"start": 2020.0, "end": 2021.5, "label": "Pre-seed", "value": 45, "color": "secondary", "annotation": "$500K"},
        {"start": 2021.5, "end": 2022.0, "label": "Pivot", "value": 20, "color": "danger", "annotation": "Market shift"},
        {"start": 2022.2, "end": 2022.5, "label": "", "value": 10, "color": "muted", "annotation": ""},
        {"start": 2022.5, "end": 2023.0, "label": "", "value": 15, "color": "muted", "annotation": "Recovery"},
        {"start": 2023.0, "end": 2024.0, "label": "Seed", "value": 60, "color": "secondary", "annotation": "$2M"},
        {"start": 2024.0, "end": 2025.2, "label": "PMF", "value": 80, "color": "success", "annotation": "Product-market fit"},
        {"start": 2025.2, "end": 2026.5, "label": "Series A", "value": 95, "color": "accent", "annotation": "$12M — Scaling"},
    ],
    "title": "Growth accelerated after pivot, with Series A marking inflection point",
    "source": "Company records; internal analysis",
    "x_label": "Time",
    "y_label": "Intensity",
}


def create_timeline_bars(data, title=None, theme_path=None, output_path=None):
    """Create a timeline chart with rectangles of varying width on a time axis."""
    theme = load_theme(theme_path)
    colors = theme["colors"]
    periods = data["periods"]

    max_val = max(p["value"] for p in periods)

    fig = go.Figure()

    # Draw each period as a rectangle (shape) + invisible scatter for hover
    for p in periods:
        color_key = p.get("color", "primary")
        fill_color = colors.get(color_key, color_key)
        x0, x1 = p["start"], p["end"]
        y0, y1 = 0, p["value"]

        # Rectangle shape
        fig.add_shape(
            type="rect",
            x0=x0, x1=x1, y0=y0, y1=y1,
            fillcolor=fill_color,
            opacity=0.85,
            line={"width": 1, "color": "white"},
        )

    # Annotations: labels and event details
    annotations_list = []
    for p in periods:
        x_mid = (p["start"] + p["end"]) / 2
        v = p["value"]
        width = p["end"] - p["start"]

        # Label ON the bar (if bar is wide enough and has a label)
        if p.get("label"):
            annotations_list.append({
                "x": x_mid,
                "y": v,
                "text": f"<b>{p['label']}</b>",
                "showarrow": False,
                "yshift": 10,
                "font": {"size": 20, "color": colors["text"], "family": "Inter Bold"},
                "xanchor": "center",
                "yanchor": "bottom",
            })

        # Event annotation above the label
        if p.get("annotation"):
            y_shift = 38 if p.get("label") else 10
            annotations_list.append({
                "x": x_mid,
                "y": v,
                "text": p["annotation"],
                "showarrow": False,
                "yshift": y_shift,
                "font": {"size": 14, "color": colors["muted"]},
                "xanchor": "center",
                "yanchor": "bottom",
            })

    # Timeline arrow
    annotations_list.append({
        "x": 1, "y": -0.07,
        "xref": "paper", "yref": "paper",
        "text": f"<b>{data.get('x_label', 'Time')} →</b>",
        "showarrow": False,
        "font": {"size": 14, "color": colors["muted"]},
        "xanchor": "right",
    })

    # Invisible scatter to establish proper axis range
    all_x = []
    for p in periods:
        all_x.extend([p["start"], p["end"]])
    fig.add_trace(go.Scatter(
        x=[min(all_x) - 0.3, max(all_x) + 0.3],
        y=[0, 0],
        mode="markers",
        marker={"size": 0.1, "opacity": 0},
        showlegend=False,
        hoverinfo="skip",
    ))

    layout = get_plotly_layout(
        theme,
        title=title or data.get("title", ""),
        source=data.get("source", ""),
    )
    layout["xaxis"] = {
        "title": "",
        "tickfont": {"size": 16, "color": colors["text"]},
        "showgrid": False,
        "showline": True,
        "linecolor": colors["muted"],
        "linewidth": 2,
        "dtick": 1,
        "range": [min(all_x) - 0.3, max(all_x) + 0.3],
    }
    layout["yaxis"] = {
        "title": {"text": data.get("y_label", "Intensity"), "font": {"size": 16}},
        "showgrid": True,
        "gridcolor": "#f0f0f0",
        "range": [0, max_val * 1.5],
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
