"""Bubble / 2x2 Matrix — Strategic Positioning.
Positions objects on two key parameters with bubble size as third dimension.
Examples: BCG matrix, risk-impact, market positioning, priority matrix.
"""
import plotly.graph_objects as go
from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "x_axis": "Market Size ($B)",
    "y_axis": "Growth Rate (%)",
    "items": [
        {"name": "AI/ML Platform", "x": 8, "y": 35, "size": 50, "color": "accent", "highlight": True},
        {"name": "Analytics SaaS", "x": 12, "y": 15, "size": 35, "color": "secondary"},
        {"name": "Data Pipeline", "x": 5, "y": 25, "size": 25, "color": "secondary"},
        {"name": "Legacy BI", "x": 15, "y": 5, "size": 40, "color": "muted"},
        {"name": "Edge Computing", "x": 3, "y": 40, "size": 15, "color": "secondary"},
        {"name": "Observability", "x": 7, "y": 28, "size": 30, "color": "secondary"},
    ],
    "quadrant_labels": {"top_right": "Stars", "top_left": "Question Marks",
                        "bottom_right": "Cash Cows", "bottom_left": "Dogs"},
    "title": "AI/ML positioned in the Stars quadrant with highest growth potential",
    "source": "Market analysis; Gartner + internal estimates",
}

def create_bubble_matrix(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]
    items = data["items"]
    fig = go.Figure()

    for item in items:
        color_key = item.get("color", "secondary")
        bubble_color = colors.get(color_key, color_key)
        is_highlight = item.get("highlight", False)
        fig.add_trace(go.Scatter(
            x=[item["x"]], y=[item["y"]], mode="markers+text",
            marker={"size": item["size"], "color": bubble_color,
                    "opacity": 0.85 if is_highlight else 0.5,
                    "line": {"width": 2, "color": "white"}},
            text=[item["name"]], textposition="top center",
            textfont={"size": 12, "color": colors["text"]},
            showlegend=False,
        ))

    all_x = [item["x"] for item in items]
    all_y = [item["y"] for item in items]
    mid_x = (min(all_x) + max(all_x)) / 2
    mid_y = (min(all_y) + max(all_y)) / 2
    fig.add_hline(y=mid_y, line={"dash": "dash", "width": 1, "color": colors["muted"]})
    fig.add_vline(x=mid_x, line={"dash": "dash", "width": 1, "color": colors["muted"]})

    quad_labels = data.get("quadrant_labels", {})
    x_range = [min(all_x) - 2, max(all_x) + 2]
    y_range = [min(all_y) - 5, max(all_y) + 5]
    quad_annotations = []
    positions = {"top_right": (x_range[1], y_range[1], "right", "top"),
                 "top_left": (x_range[0], y_range[1], "left", "top"),
                 "bottom_right": (x_range[1], y_range[0], "right", "bottom"),
                 "bottom_left": (x_range[0], y_range[0], "left", "bottom")}
    for key, label in quad_labels.items():
        if key in positions:
            px, py, xa, ya = positions[key]
            quad_annotations.append({"x": px, "y": py, "text": label, "xanchor": xa, "yanchor": ya,
                                     "font": {"size": 14, "color": colors["muted"]}, "showarrow": False})

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["xaxis"] = {"title": data["x_axis"], "showgrid": True, "gridcolor": "#f0f0f0", "range": x_range}
    layout["yaxis"] = {"title": data["y_axis"], "showgrid": True, "gridcolor": "#f0f0f0", "range": y_range}
    layout["annotations"] = layout.get("annotations", []) + quad_annotations
    fig.update_layout(**layout)
    if output_path:
        save_chart(fig, output_path)
    return fig

if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data: data = DEMO_DATA
    create_bubble_matrix(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
