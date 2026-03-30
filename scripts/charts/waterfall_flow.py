"""Waterfall Flow — Cumulative Contribution Analysis.
Shows how individual positive/negative factors contribute to a final result.
Examples: revenue bridge, cost breakdown, P&L waterfall, budget variance,
factor influence analysis, before/after decomposition.
"""
import plotly.graph_objects as go
from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "items": [
        {"name": "Starting Revenue", "value": 100, "measure": "absolute"},
        {"name": "New Customers", "value": 45, "measure": "relative"},
        {"name": "Upsells", "value": 25, "measure": "relative"},
        {"name": "Price Increase", "value": 15, "measure": "relative"},
        {"name": "Churn", "value": -30, "measure": "relative"},
        {"name": "Downgrades", "value": -12, "measure": "relative"},
        {"name": "FX Impact", "value": -8, "measure": "relative"},
        {"name": "Ending Revenue", "value": 135, "measure": "total"},
    ],
    "title": "New customers drove $45M growth, partially offset by $30M churn",
    "source": "Finance team; FY2026 revenue bridge",
}


def create_waterfall_flow(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]

    items = data["items"]
    names = [item["name"] for item in items]
    values = [item["value"] for item in items]
    measures = [item["measure"] for item in items]

    # Color: green for positive, red for negative, blue for totals
    text_values = []
    for item in items:
        v = item["value"]
        if item["measure"] == "relative":
            text_values.append(f"+${v}M" if v > 0 else f"-${abs(v)}M")
        else:
            text_values.append(f"${v}M")

    fig = go.Figure(go.Waterfall(
        name="Revenue",
        orientation="v",
        measure=measures,
        x=names,
        y=values,
        text=text_values,
        textposition="outside",
        textfont={"size": 18, "color": colors["text"], "family": "Inter Bold"},
        connector={"line": {"color": colors["muted"], "width": 1.5, "dash": "dot"}},
        increasing={"marker": {"color": colors["success"]}},
        decreasing={"marker": {"color": colors["danger"]}},
        totals={"marker": {"color": colors["primary"]}},
    ))

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["yaxis"] = {"title": "Revenue ($M)", "showgrid": True, "gridcolor": "#f0f0f0",
                        "title_font": {"size": 16}, "tickfont": {"size": 14}}
    layout["xaxis"] = {"title": "", "tickangle": -25, "tickfont": {"size": 14}}
    layout["showlegend"] = False
    fig.update_layout(**layout)

    if output_path:
        save_chart(fig, output_path)
    return fig


if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data:
        data = DEMO_DATA
    create_waterfall_flow(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
