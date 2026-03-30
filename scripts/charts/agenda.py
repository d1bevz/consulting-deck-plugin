"""Agenda — Navigation / Table of Contents.
Shows presentation structure with sections and subsections.
"""
import plotly.graph_objects as go
from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "sections": [
        {"title": "Market Opportunity", "subsections": ["Market size", "Growth trends", "Key segments"]},
        {"title": "Our Solution", "subsections": ["Product overview", "Key differentiators"]},
        {"title": "Traction & Metrics", "subsections": ["Revenue growth", "Customer pipeline", "Unit economics"]},
        {"title": "Go-to-Market", "subsections": ["Sales strategy", "Partnerships"]},
        {"title": "Ask & Timeline", "subsections": ["Funding ask", "Milestones"]},
    ],
    "title": "Agenda",
    "highlight_index": None,
}

def create_agenda(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]
    sections = data["sections"]
    highlight_idx = data.get("highlight_index")
    fig = go.Figure()
    annotations = []

    n_sections = len(sections)
    start_y = 0.82
    spacing = 0.75 / max(n_sections, 1)

    for i, section in enumerate(sections):
        y_pos = start_y - i * spacing
        is_highlight = (highlight_idx is not None and i == highlight_idx)
        num_color = colors["accent"] if is_highlight else colors["primary"]

        annotations.append({"x": 0.08, "y": y_pos, "text": f"<b>{i + 1:02d}</b>",
            "font": {"size": 28, "color": num_color},
            "xref": "paper", "yref": "paper", "showarrow": False, "xanchor": "center"})

        title_weight = "<b>" if is_highlight else ""
        title_end = "</b>" if is_highlight else ""
        annotations.append({"x": 0.15, "y": y_pos,
            "text": f"{title_weight}{section['title']}{title_end}",
            "font": {"size": 22, "color": colors["text"]},
            "xref": "paper", "yref": "paper", "showarrow": False, "xanchor": "left"})

        subs = section.get("subsections", [])
        if subs:
            annotations.append({"x": 0.15, "y": y_pos - 0.04,
                "text": " · ".join(subs), "font": {"size": 13, "color": colors["muted"]},
                "xref": "paper", "yref": "paper", "showarrow": False, "xanchor": "left"})

        if i < n_sections - 1:
            fig.add_shape(type="line", x0=0.08, x1=0.92,
                y0=y_pos - spacing / 2 - 0.02, y1=y_pos - spacing / 2 - 0.02,
                xref="paper", yref="paper", line={"color": "#f0f0f0", "width": 1})

    layout = get_plotly_layout(theme, title=title or data.get("title", "Agenda"), source="")
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
    create_agenda(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
