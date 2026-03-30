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

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years, y=values, marker_color=bar_colors,
        text=labels, textposition="outside",
        textfont={"size": 13, "color": colors["text"]},
    ))

    annotations_list = []
    for p in periods:
        if p.get("annotation"):
            annotations_list.append({
                "x": p["year"], "y": p["value"] + 8,
                "text": p["annotation"], "showarrow": False,
                "font": {"size": 11, "color": colors["muted"]},
            })

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["yaxis"] = {"title": "Intensity", "showgrid": True, "gridcolor": "#f0f0f0", "range": [0, max(values) * 1.3]}
    layout["xaxis"] = {"title": ""}
    layout["showlegend"] = False
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
