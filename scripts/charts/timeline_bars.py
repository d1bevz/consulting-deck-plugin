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

    n = len(periods)
    x_indices = list(range(n))
    years = [p["year"] for p in periods]
    values = [p["value"] for p in periods]
    bar_colors = [
        colors.get(p.get("color", "primary"), colors["primary"])
        for p in periods
    ]
    max_val = max(values)

    # --- Main bar chart (integer x positions, categorical tick labels) ---
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x_indices,
        y=values,
        marker_color=bar_colors,
        width=[0.7] * n,
        # Value numbers displayed ABOVE each bar
        text=[f"<b>{v}</b>" for v in values],
        textposition="outside",
        textfont=dict(size=20, color=colors["text"], family="Inter Bold"),
    ))

    # --- Annotations ---
    annotations_list = []

    for i, p in enumerate(periods):
        v = p["value"]
        label = p["label"]

        # Label INSIDE the bar — large, white, bold
        annotations_list.append(dict(
            x=i,
            y=v / 2,
            text=f"<b>{label}</b>",
            showarrow=False,
            font=dict(size=18, color="#ffffff", family="Inter Bold"),
            xanchor="center",
            yanchor="middle",
        ))

        # Event annotation BELOW the x-axis label (small callout)
        if p.get("annotation"):
            annotations_list.append(dict(
                x=i,
                y=-max_val * 0.09,
                text=p["annotation"],
                showarrow=False,
                font=dict(size=13, color=colors["muted"], family="Inter Regular"),
                xanchor="center",
                yanchor="top",
            ))

    # --- Layout ---
    layout = get_plotly_layout(
        theme,
        title=title or data.get("title", ""),
        source=data.get("source", ""),
    )
    layout["xaxis"] = dict(
        title="",
        tickmode="array",
        tickvals=x_indices,
        ticktext=years,
        tickfont=dict(size=16, color=colors["text"]),
        range=[-0.6, n - 0.4],
    )
    layout["yaxis"] = dict(
        title=dict(text="Intensity", font=dict(size=16)),
        showgrid=True,
        gridcolor="#f0f0f0",
        range=[-(max_val * 0.15), max_val * 1.20],
        tickfont=dict(size=14),
    )
    layout["showlegend"] = False
    layout["bargap"] = 0.3
    layout["margin"] = dict(l=80, r=60, t=120, b=120)
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
