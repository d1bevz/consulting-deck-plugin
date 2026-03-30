"""Driver Tree — KPI Decomposition.
Decomposes a complex metric into components with status assessment.
Examples: revenue drivers, root cause analysis, product-market fit.
"""
import plotly.graph_objects as go
from scripts.utils import load_theme, get_plotly_layout, save_chart, parse_cli_args

DEMO_DATA = {
    "tree": {
        "node": "Revenue Growth",
        "status": "partial",
        "children": [
            {"node": "New Customers", "status": "met", "children": [
                {"node": "Organic Traffic", "status": "met", "children": []},
                {"node": "Paid Acquisition", "status": "met", "children": []},
                {"node": "Referrals", "status": "partial", "children": []},
            ]},
            {"node": "Retention", "status": "unmet", "children": [
                {"node": "Onboarding", "status": "met", "children": []},
                {"node": "Engagement", "status": "unmet", "children": []},
                {"node": "Churn Prevention", "status": "unmet", "children": []},
            ]},
            {"node": "ARPU", "status": "met", "children": [
                {"node": "Pricing", "status": "met", "children": []},
                {"node": "Upsell", "status": "partial", "children": []},
            ]},
        ],
    },
    "title": "Revenue growth limited by retention — engagement and churn are key gaps",
    "source": "Product analytics; Q1 2026",
}

STATUS_COLORS = {"met": "success", "unmet": "danger", "partial": "warning"}
STATUS_LABELS = {"met": "\u2713 Met", "unmet": "\u2717 Unmet", "partial": "~ Partial"}


def _flatten_tree(tree, parent=None, edges=None, nodes=None):
    if edges is None: edges = []
    if nodes is None: nodes = []
    node_id = tree["node"]
    nodes.append({"id": node_id, "status": tree["status"]})
    if parent:
        edges.append((parent, node_id))
    for child in tree.get("children", []):
        _flatten_tree(child, parent=node_id, edges=edges, nodes=nodes)
    return nodes, edges


def _compute_positions(tree, x_start=0, x_end=1, y=0, y_step=1.0, positions=None):
    """Recursive positioning: each node centered above its children's span."""
    if positions is None:
        positions = {}
    node_id = tree["node"]
    children = tree.get("children", [])

    if not children:
        x_center = (x_start + x_end) / 2
        positions[node_id] = (x_center, -y)
        return positions

    # Divide horizontal space equally among children
    child_width = (x_end - x_start) / len(children)
    for idx, child in enumerate(children):
        cx_start = x_start + idx * child_width
        cx_end = cx_start + child_width
        _compute_positions(child, cx_start, cx_end, y + y_step, y_step, positions)

    # Center parent above its children
    child_xs = [positions[c["node"]][0] for c in children]
    x_center = (min(child_xs) + max(child_xs)) / 2
    positions[node_id] = (x_center, -y)
    return positions


def create_driver_tree(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]
    nodes_list, edges = _flatten_tree(data["tree"])
    node_statuses = {n["id"]: n["status"] for n in nodes_list}

    # Compute positions with recursive algorithm for clean top-to-bottom layout
    pos = _compute_positions(data["tree"], x_start=0, x_end=10, y=0, y_step=1.5)

    fig = go.Figure()

    # Draw connecting lines (thicker, with slight curve via intermediate points)
    for u, v in edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        # Stepped path: go down halfway, then across, then down
        mid_y = (y0 + y1) / 2
        fig.add_trace(go.Scatter(
            x=[x0, x0, x1, x1], y=[y0, mid_y, mid_y, y1],
            mode="lines",
            line={"width": 2.5, "color": colors["muted"], "shape": "spline"},
            showlegend=False, hoverinfo="skip",
        ))

    # Determine root node for special styling
    root_id = data["tree"]["node"]

    # Draw nodes with status labels
    for node_info in nodes_list:
        nid = node_info["id"]
        status = node_info["status"]
        x, y = pos[nid]
        color_key = STATUS_COLORS.get(status, "muted")
        node_color = colors.get(color_key, color_key)
        status_label = STATUS_LABELS.get(status, "")

        is_root = nid == root_id
        marker_size = 48 if is_root else 30
        text_size = 16 if is_root else 14
        font_weight = "bold" if is_root else "normal"

        # Node marker
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="markers",
            marker={
                "size": marker_size,
                "color": node_color,
                "line": {"width": 3 if is_root else 2, "color": "white"},
            },
            showlegend=False,
            hovertext=f"<b>{nid}</b><br>Status: {status_label}",
            hoverinfo="text",
        ))

        # Node label — positioned to the right of the node
        label_text = f"<b>{nid}</b>" if is_root else nid
        fig.add_annotation(
            x=x, y=y,
            text=f"{label_text}  <span style='color:{node_color}'>{status_label}</span>",
            showarrow=False,
            xanchor="left",
            xshift=marker_size // 2 + 8,
            font={"size": text_size, "color": colors["text"]},
        )

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["xaxis"] = {"visible": False}
    layout["yaxis"] = {"visible": False}
    layout["showlegend"] = False
    fig.update_layout(**layout)

    if output_path:
        save_chart(fig, output_path)
    return fig

if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data: data = DEMO_DATA
    create_driver_tree(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
