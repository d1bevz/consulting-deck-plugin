"""Ranked Bars — Competitive Ranking.
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


def create_ranked_bars(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]
    items = sorted(data["items"], key=lambda x: x["value"], reverse=True)
    names = [item["name"] for item in items]
    values = [item["value"] for item in items]
    leader_value = values[0]
    max_val = max(values)
    avg_value = sum(values) / len(values)

    # Colors: highlighted bars get accent + bold border, rest muted
    bar_colors = [colors["accent"] if item["highlight"] else colors["muted"] for item in items]
    border_colors = [colors["text"] if item["highlight"] else "rgba(0,0,0,0)" for item in items]
    border_widths = [3 if item["highlight"] else 0 for item in items]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names,
        y=values,
        marker_color=bar_colors,
        marker_line_color=border_colors,
        marker_line_width=border_widths,
        width=[0.7 if item["highlight"] else 0.6 for item in items],
        text=[str(v) for v in values],
        textposition="outside",
        textfont={"size": 15, "color": colors["text"], "family": "Inter Bold"},
    ))

    # Horizontal average line
    fig.add_shape(
        type="line",
        x0=-0.5, x1=len(items) - 0.5,
        y0=avg_value, y1=avg_value,
        line={"color": colors["warning"], "width": 2, "dash": "dash"},
    )

    annotations_list = []

    # Average line label
    annotations_list.append({
        "x": len(items) - 1, "y": avg_value,
        "text": f"Avg: {avg_value:.0f}",
        "showarrow": False,
        "xanchor": "left",
        "yanchor": "bottom",
        "xshift": 30,
        "font": {"size": 13, "color": colors["warning"], "family": "Inter SemiBold"},
    })

    # Rank numbers and delta-from-leader annotations
    for i, item in enumerate(items):
        rank = i + 1
        v = item["value"]

        # Rank number below bar name
        annotations_list.append({
            "x": item["name"], "y": -(max_val * 0.04),
            "text": f"<b>#{rank}</b>",
            "showarrow": False,
            "font": {"size": 13, "color": colors["accent"] if item["highlight"] else colors["muted"]},
            "xanchor": "center", "yanchor": "top",
        })

        # Delta from leader (skip rank #1)
        if rank > 1:
            delta = v - leader_value
            annotations_list.append({
                "x": item["name"], "y": v + max_val * 0.10,
                "text": f"{delta:+d}",
                "showarrow": False,
                "font": {"size": 12, "color": colors["danger"] if delta < -20 else colors["muted"]},
                "xanchor": "center", "yanchor": "bottom",
            })

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["yaxis"] = {
        "title": {"text": "Score", "font": {"size": 14}},
        "showgrid": True,
        "gridcolor": "#f0f0f0",
        "range": [-(max_val * 0.08), max_val * 1.3],
        "tickfont": {"size": 13},
    }
    layout["xaxis"] = {
        "title": "",
        "tickangle": -25,
        "tickfont": {"size": 12},
    }
    layout["showlegend"] = False
    layout["bargap"] = 0.25
    layout["margin"] = {"l": 80, "r": 80, "t": 120, "b": 110}
    layout["annotations"] = layout.get("annotations", []) + annotations_list
    fig.update_layout(**layout)

    if output_path:
        save_chart(fig, output_path)
    return fig


# Keep backward-compatible alias
create_waterfall = create_ranked_bars


if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data:
        data = DEMO_DATA
    create_ranked_bars(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
