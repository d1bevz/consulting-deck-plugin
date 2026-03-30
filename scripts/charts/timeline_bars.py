"""Timeline Bars — Historical Evolution.
Shows how a metric changed over time with key events.
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
    theme = load_theme(theme_path)
    colors = theme["colors"]
    periods = data["periods"]
    years = [p["year"] for p in periods]
    values = [p["value"] for p in periods]
    labels = [p["label"] for p in periods]
    bar_colors = [colors.get(p.get("color", "primary"), p.get("color", colors["primary"])) for p in periods]
    max_val = max(values)

    # Determine label placement: inside bar if bar is tall enough, otherwise below x-axis
    label_threshold = max_val * 0.15  # bars shorter than 15% of max get label below

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years,
        y=values,
        marker_color=bar_colors,
        text=[str(v) for v in values],
        textposition="outside",
        textfont={"size": 16, "color": colors["text"], "family": "Inter Bold"},
    ))

    annotations_list = []

    for i, p in enumerate(periods):
        v = p["value"]
        label = p["label"]

        # Use index for x position (category axis maps strings to 0-based indices)
        # Place label inside bar if tall enough, otherwise below x-axis
        if v >= label_threshold:
            annotations_list.append({
                "x": i, "y": v / 2,
                "text": f"<b>{label}</b>",
                "showarrow": False,
                "font": {"size": 14, "color": "#ffffff"},
                "xanchor": "center", "yanchor": "middle",
            })
        else:
            annotations_list.append({
                "x": i, "y": -max_val * 0.06,
                "text": f"<b>{label}</b>",
                "showarrow": False,
                "font": {"size": 13, "color": colors["text"]},
                "xanchor": "center", "yanchor": "top",
            })

        # Event annotations above bars (with offset from value label)
        if p.get("annotation"):
            annotations_list.append({
                "x": i, "y": v + max_val * 0.14,
                "text": p["annotation"],
                "showarrow": True,
                "arrowhead": 0,
                "arrowwidth": 1,
                "arrowcolor": colors["muted"],
                "ax": 0, "ay": -20,
                "font": {"size": 12, "color": colors["muted"]},
                "xanchor": "center",
            })

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["yaxis"] = {
        "title": {"text": "Intensity", "font": {"size": 14}},
        "showgrid": True,
        "gridcolor": "#f0f0f0",
        "range": [-(max_val * 0.1), max_val * 1.45],
        "tickfont": {"size": 13},
    }
    layout["xaxis"] = {
        "title": "",
        "tickfont": {"size": 14},
        "type": "category",
        "categoryorder": "array",
        "categoryarray": years,
    }
    layout["showlegend"] = False
    layout["bargap"] = 0.3
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
