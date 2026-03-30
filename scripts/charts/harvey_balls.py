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
HARVEY_UNICODE = ["\u25cb", "\u25d4", "\u25d1", "\u25d5", "\u25cf"]  # ○ ◔ ◑ ◕ ●
FILL_LABELS = ["Empty (0/4)", "Quarter (1/4)", "Half (2/4)", "Three-quarter (3/4)", "Full (4/4)"]

BALL_SIZE = 42
COL_SPACING = 1.2
ROW_SPACING = 1.2


def create_harvey_balls(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]
    rows = data["rows"]
    columns = data["columns"]
    scores = data["scores"]

    # Find the "best" row (highest total score) for highlighting
    row_totals = [sum(row) for row in scores]
    best_row_idx = row_totals.index(max(row_totals))

    fig = go.Figure()

    n_rows = len(rows)
    n_cols = len(columns)

    # Draw alternating row backgrounds for readability
    for i in range(n_rows):
        y_pos = (n_rows - 1 - i) * ROW_SPACING
        is_best = i == best_row_idx
        if is_best:
            bg_color = "rgba(22, 199, 154, 0.10)"  # subtle green highlight for best row
        elif i % 2 == 0:
            bg_color = "rgba(139, 157, 195, 0.07)"  # subtle alternating band
        else:
            bg_color = "rgba(0, 0, 0, 0)"
        fig.add_shape(
            type="rect",
            x0=-1.5, x1=(n_cols - 1) * COL_SPACING + 0.7,
            y0=y_pos - ROW_SPACING / 2, y1=y_pos + ROW_SPACING / 2,
            fillcolor=bg_color, line_width=0, layer="below",
        )

    # Draw balls
    for i, row in enumerate(rows):
        for j, col in enumerate(columns):
            score = scores[i][j]
            fill_ratio = HARVEY_SIZES[score]
            x_pos = j * COL_SPACING
            y_pos = (n_rows - 1 - i) * ROW_SPACING

            # Background circle (empty ball)
            fig.add_trace(go.Scatter(
                x=[x_pos], y=[y_pos], mode="markers",
                marker={
                    "size": BALL_SIZE,
                    "color": "#e8e8e8",
                    "line": {"width": 1.5, "color": colors["muted"]},
                },
                showlegend=False,
                hovertext=f"<b>{row} / {col}</b><br>{HARVEY_UNICODE[score]} {score}/4 — {FILL_LABELS[score]}",
                hoverinfo="text",
            ))
            # Filled portion
            if score > 0:
                fig.add_trace(go.Scatter(
                    x=[x_pos], y=[y_pos], mode="markers",
                    marker={"size": BALL_SIZE * fill_ratio, "color": colors["primary"]},
                    showlegend=False, hoverinfo="skip",
                ))

    # Legend — show what each fill level means
    legend_y = -1.2 * ROW_SPACING  # below the matrix
    legend_start_x = 0.0
    legend_spacing = 1.6
    for lvl in range(5):
        lx = legend_start_x + lvl * legend_spacing
        ratio = HARVEY_SIZES[lvl]
        # Background circle
        fig.add_trace(go.Scatter(
            x=[lx], y=[legend_y], mode="markers",
            marker={"size": 22, "color": "#e8e8e8", "line": {"width": 1, "color": colors["muted"]}},
            showlegend=False, hoverinfo="skip",
        ))
        if lvl > 0:
            fig.add_trace(go.Scatter(
                x=[lx], y=[legend_y], mode="markers",
                marker={"size": 22 * ratio, "color": colors["primary"]},
                showlegend=False, hoverinfo="skip",
            ))
        fig.add_annotation(
            x=lx, y=legend_y,
            text=f"{lvl}/4",
            showarrow=False, yshift=-22,
            font={"size": 11, "color": colors["muted"]},
        )

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["xaxis"] = {
        "tickvals": [j * COL_SPACING for j in range(n_cols)],
        "ticktext": [f"<b>{c}</b>" for c in columns],
        "tickfont": {"size": 14, "color": colors["text"]},
        "side": "top",
        "showgrid": False,
        "zeroline": False,
        "range": [-1.5, (n_cols - 1) * COL_SPACING + 0.8],
    }
    layout["yaxis"] = {
        "tickvals": [(n_rows - 1 - i) * ROW_SPACING for i in range(n_rows)],
        "ticktext": [f"<b>{r}</b>" for r in rows],
        "tickfont": {"size": 16, "color": colors["text"]},
        "showgrid": False,
        "zeroline": False,
        "range": [legend_y - ROW_SPACING, (n_rows - 1) * ROW_SPACING + ROW_SPACING * 0.7],
    }
    layout["showlegend"] = False
    layout["margin"] = {"l": 160, "r": 60, "t": 100, "b": 80}
    fig.update_layout(**layout)

    if output_path:
        save_chart(fig, output_path)
    return fig

if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data: data = DEMO_DATA
    create_harvey_balls(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
