"""Stakeholder Quotes — Voice of Customer.
Structured pro/contra quotes with synthesis.
Examples: customer interviews, market research, internal feedback.
"""
import plotly.graph_objects as go
from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "pro": [
        {"quote": "Reduced our processing time by 60%", "source": "CTO, FinTech Co"},
        {"quote": "Best onboarding experience we've seen", "source": "VP Product, RetailCo"},
        {"quote": "Finally, an API that just works", "source": "Lead Engineer, HealthTech"},
    ],
    "contra": [
        {"quote": "Pricing is hard to predict at scale", "source": "CFO, Enterprise Client"},
        {"quote": "Documentation could be more detailed", "source": "Junior Developer, Agency"},
        {"quote": "Missing some advanced customization options", "source": "Architect, Consulting Firm"},
    ],
    "summary": "Strong product-market fit validated; pricing transparency and docs are the main improvement areas",
    "pro_header": "What's working",
    "contra_header": "Areas to improve",
    "title": "Customer feedback is overwhelmingly positive, with pricing as the main concern",
    "source": "Customer interviews; N=24, Q1 2026",
}

def create_stakeholder_quotes(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]
    fig = go.Figure()
    annotations = []

    pro_header = data.get("pro_header", "Positive")
    contra_header = data.get("contra_header", "Concerns")

    annotations.append({"x": 0.22, "y": 0.88, "text": f"<b>{pro_header}</b>",
        "font": {"size": 20, "color": colors["success"]},
        "xref": "paper", "yref": "paper", "showarrow": False})
    annotations.append({"x": 0.72, "y": 0.88, "text": f"<b>{contra_header}</b>",
        "font": {"size": 20, "color": colors["danger"]},
        "xref": "paper", "yref": "paper", "showarrow": False})

    for i, q in enumerate(data["pro"]):
        y_pos = 0.78 - i * 0.18
        annotations.append({"x": 0.05, "y": y_pos, "text": f'"{q["quote"]}"',
            "font": {"size": 15, "color": colors["text"]},
            "xref": "paper", "yref": "paper", "showarrow": False, "xanchor": "left"})
        annotations.append({"x": 0.05, "y": y_pos - 0.05, "text": f"— {q['source']}",
            "font": {"size": 12, "color": colors["muted"]},
            "xref": "paper", "yref": "paper", "showarrow": False, "xanchor": "left"})

    for i, q in enumerate(data["contra"]):
        y_pos = 0.78 - i * 0.18
        annotations.append({"x": 0.55, "y": y_pos, "text": f'"{q["quote"]}"',
            "font": {"size": 15, "color": colors["text"]},
            "xref": "paper", "yref": "paper", "showarrow": False, "xanchor": "left"})
        annotations.append({"x": 0.55, "y": y_pos - 0.05, "text": f"— {q['source']}",
            "font": {"size": 12, "color": colors["muted"]},
            "xref": "paper", "yref": "paper", "showarrow": False, "xanchor": "left"})

    fig.add_shape(type="line", x0=0.5, x1=0.5, y0=0.15, y1=0.9,
        xref="paper", yref="paper", line={"color": colors["muted"], "width": 1, "dash": "dot"})

    if data.get("summary"):
        annotations.append({"x": 0.5, "y": 0.05, "text": f"<b>{data['summary']}</b>",
            "font": {"size": 14, "color": colors["text"]},
            "xref": "paper", "yref": "paper", "showarrow": False,
            "bgcolor": "#f5f5f5", "bordercolor": colors["muted"], "borderpad": 12, "borderwidth": 1})

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["xaxis"] = {"visible": False, "range": [0, 1]}
    layout["yaxis"] = {"visible": False, "range": [0, 1]}
    layout["annotations"] = layout.get("annotations", []) + annotations
    fig.update_layout(**layout)
    if output_path:
        save_chart(fig, output_path)
    return fig

if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data: data = DEMO_DATA
    create_stakeholder_quotes(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
