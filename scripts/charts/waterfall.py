"""Waterfall / Ranked Bars — Competitive Ranking.
Positions an object among competitors/alternatives in descending order.
Examples: NPS benchmark, feature comparison, customer satisfaction ranking.
"""
import plotly.graph_objects as go
from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "items": [
        {"name": "Competitor A", "value": 92, "highlight": False},
        {"name": "Our Product", "value": 87, "highlight": True},
        {"name": "Competitor B", "value": 83, "highlight": False},
        {"name": "Competitor C", "value": 78, "highlight": False},
        {"name": "Competitor D", "value": 71, "highlight": False},
        {"name": "Industry Avg", "value": 65, "highlight": False},
        {"name": "Competitor E", "value": 58, "highlight": False},
        {"name": "Competitor F", "value": 52, "highlight": False},
        {"name": "Our Product (2024)", "value": 45, "highlight": True},
        {"name": "Competitor G", "value": 38, "highlight": False},
    ],
    "title": "Our product ranks #2 overall, up from #9 last year",
    "source": "Customer satisfaction survey; Q1 2026",
}


def create_waterfall(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]
    items = sorted(data["items"], key=lambda x: x["value"], reverse=True)
    names = [item["name"] for item in items]
    values = [item["value"] for item in items]
    bar_colors = [colors["accent"] if item["highlight"] else colors["muted"] for item in items]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names, y=values, marker_color=bar_colors,
        text=[str(v) for v in values], textposition="outside",
        textfont={"size": 12, "color": colors["text"]},
    ))

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["yaxis"] = {"title": "Score", "showgrid": True, "gridcolor": "#f0f0f0", "range": [0, max(values) * 1.2]}
    layout["xaxis"] = {"title": "", "tickangle": -30}
    layout["showlegend"] = False
    fig.update_layout(**layout)

    if output_path:
        save_chart(fig, output_path)
    return fig


if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data:
        data = DEMO_DATA
    create_waterfall(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
