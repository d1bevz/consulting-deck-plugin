"""Harvey Ball Matrix — Qualitative Scoring.
Scores multiple objects against qualitative criteria.
Examples: vendor evaluation, technology comparison, hiring scorecard.
"""
import plotly.graph_objects as go
from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "rows": ["Our Product", "Vendor A", "Vendor B", "Vendor C", "Open Source"],
    "columns": ["Scalability", "Security", "Cost", "Support", "Integration", "Docs"],
    "scores": [
        [4, 3, 2, 4, 3, 3],
        [3, 4, 3, 2, 4, 2],
        [2, 2, 4, 3, 2, 4],
        [3, 3, 3, 3, 3, 3],
        [2, 1, 4, 1, 3, 2],
    ],
    "title": "Our product leads in support and scalability; cost is the trade-off",
    "source": "Technology evaluation matrix; Engineering team",
}

HARVEY_SIZES = [0.0, 0.25, 0.5, 0.75, 1.0]

def create_harvey_balls(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]
    rows = data["rows"]
    columns = data["columns"]
    scores = data["scores"]

    fig = go.Figure()
    for i, row in enumerate(rows):
        for j, col in enumerate(columns):
            score = scores[i][j]
            fill_ratio = HARVEY_SIZES[score]
            fig.add_trace(go.Scatter(
                x=[j], y=[len(rows) - 1 - i], mode="markers",
                marker={"size": 32, "color": "#e8e8e8", "line": {"width": 1.5, "color": colors["muted"]}},
                showlegend=False, hovertext=f"{row} / {col}: {score}/4", hoverinfo="text",
            ))
            if score > 0:
                fig.add_trace(go.Scatter(
                    x=[j], y=[len(rows) - 1 - i], mode="markers",
                    marker={"size": 32 * fill_ratio, "color": colors["primary"]},
                    showlegend=False, hoverinfo="skip",
                ))

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["xaxis"] = {"tickvals": list(range(len(columns))), "ticktext": columns, "side": "top",
                        "showgrid": False, "zeroline": False, "range": [-0.8, len(columns) - 0.2]}
    layout["yaxis"] = {"tickvals": list(range(len(rows))), "ticktext": list(reversed(rows)),
                        "showgrid": False, "zeroline": False, "range": [-0.8, len(rows) - 0.2]}
    layout["showlegend"] = False
    fig.update_layout(**layout)
    if output_path:
        save_chart(fig, output_path)
    return fig

if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data: data = DEMO_DATA
    create_harvey_balls(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
