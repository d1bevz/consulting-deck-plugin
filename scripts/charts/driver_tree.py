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


def _collect_leaves(tree, leaves=None):
    """Return set of leaf node IDs."""
    if leaves is None:
        leaves = set()
    if not tree.get("children"):
        leaves.add(tree["node"])
    for child in tree.get("children", []):
        _collect_leaves(child, leaves)
    return leaves


def create_driver_tree(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]
    nodes_list, edges = _flatten_tree(data["tree"])
    node_statuses = {n["id"]: n["status"] for n in nodes_list}
    leaf_ids = _collect_leaves(data["tree"])

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

    # Draw nodes with status labels — sizes increased ~20%
    for node_info in nodes_list:
        nid = node_info["id"]
        status = node_info["status"]
        x, y = pos[nid]
        color_key = STATUS_COLORS.get(status, "muted")
        node_color = colors.get(color_key, color_key)
        status_label = STATUS_LABELS.get(status, "")

        is_root = nid == root_id
        is_leaf = nid in leaf_ids
        marker_size = 56 if is_root else 36
        text_size = 26 if is_root else (20 if is_leaf else 22)

        # Leaf nodes: marker + text below via mode="markers+text"
        if is_leaf:
            display_text = f"{nid}<br>{status_label}"
            fig.add_trace(go.Scatter(
                x=[x], y=[y], mode="markers+text",
                marker={
                    "size": marker_size,
                    "color": node_color,
                    "line": {"width": 2, "color": "white"},
                },
                text=[display_text],
                textposition="bottom center",
                textfont={"size": text_size, "color": colors["text"]},
                showlegend=False,
                hovertext=f"<b>{nid}</b><br>Status: {status_label}",
                hoverinfo="text",
            ))
        else:
            # Non-leaf: marker + text to the right
            display_text = f"<b>{nid}</b>  {status_label}" if is_root else f"{nid}  {status_label}"
            fig.add_trace(go.Scatter(
                x=[x], y=[y], mode="markers+text",
                marker={
                    "size": marker_size,
                    "color": node_color,
                    "line": {"width": 3 if is_root else 2, "color": "white"},
                },
                text=[display_text],
                textposition="middle right",
                textfont={"size": text_size, "color": colors["text"]},
                showlegend=False,
                hovertext=f"<b>{nid}</b><br>Status: {status_label}",
                hoverinfo="text",
            ))

    # Compute axis ranges with padding for labels
    all_x = [pos[n["id"]][0] for n in nodes_list]
    all_y = [pos[n["id"]][1] for n in nodes_list]
    x_pad = (max(all_x) - min(all_x)) * 0.12
    y_range_span = max(all_y) - min(all_y) if max(all_y) != min(all_y) else 1
    # Extra space below for leaf labels, extra space above for root label
    y_pad_bottom = y_range_span * 0.25
    y_pad_top = y_range_span * 0.15

    layout = get_plotly_layout(theme, title=title or data.get("title", ""), source=data.get("source", ""))
    layout["xaxis"] = {"visible": False, "range": [min(all_x) - x_pad, max(all_x) + x_pad]}
    layout["yaxis"] = {"visible": False, "range": [min(all_y) - y_pad_bottom, max(all_y) + y_pad_top]}
    layout["showlegend"] = False
    # Extra bottom margin to accommodate leaf labels below nodes
    layout["margin"] = {"l": 80, "r": 80, "t": 100, "b": 140}
    fig.update_layout(**layout)

    if output_path:
        save_chart(fig, output_path)
    return fig

if __name__ == "__main__":
    data, output, theme_path = parse_cli_args()
    if not data: data = DEMO_DATA
    create_driver_tree(data, output_path=output, theme_path=theme_path)
    print(f"Saved to {output}")
