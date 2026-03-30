"""Mekko Chart — Variable-Width Bar Chart (two dimensions per bar).

Each bar encodes TWO numeric values:
- WIDTH = one dimension (market size, revenue, duration, segment share)
- HEIGHT = another dimension (growth rate, margin, intensity, score)

Inspired by BCG "Romance" slide. Also known as Marimekko chart,
width-encoded bar chart, or variable-width column chart.

Examples:
- Market segments: width=market size, height=growth rate
- Client portfolio: width=revenue, height=margin
- Project timeline: width=duration, height=complexity
- Product lines: width=units sold, height=avg price
"""

import plotly.graph_objects as go

from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "periods": [
        {"start": 0, "end": 25, "label": "Enterprise", "value": 12, "color": "primary", "annotation": "$25B market"},
        {"start": 25, "end": 43, "label": "Mid-Market", "value": 28, "color": "accent", "annotation": "$18B market"},
        {"start": 43, "end": 55, "label": "SMB", "value": 35, "color": "success", "annotation": "$12B market"},
        {"start": 55, "end": 70, "label": "Prosumer", "value": 22, "color": "secondary", "annotation": "$15B market"},
        {"start": 70, "end": 85, "label": "Consumer", "value": 8, "color": "muted", "annotation": "$15B market"},
        {"start": 85, "end": 100, "label": "Free Tier", "value": 3, "color": "muted", "annotation": "$15B market"},
    ],
    "title": "Mid-market and SMB segments show highest growth despite smaller market size",
    "source": "Market analysis; Gartner 2026",
    "x_label": "Market Share (%)",
    "y_label": "Growth Rate (%)",
}


def create_mekko(data, title=None, theme_path=None, output_path=None):
    """Create a Mekko chart — variable-width bars encoding two dimensions."""
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


# Backward compatibility
create_timeline_bars = create_mekko


if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data:
        data = DEMO_DATA
    create_mekko(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
