"""Driver Tree — KPI Decomposition.
Decomposes a complex metric into components with status assessment.
Examples: revenue drivers, root cause analysis, product-market fit.
"""
import plotly.graph_objects as go
import networkx as nx
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

def create_driver_tree(data, title=None, theme_path=None, output_path=None):
    theme = load_theme(theme_path)
    colors = theme["colors"]
    nodes_list, edges = _flatten_tree(data["tree"])
    node_statuses = {n["id"]: n["status"] for n in nodes_list}

    G = nx.DiGraph()
    G.add_edges_from(edges)

    def assign_depth(tree, depth=0, depths=None):
        if depths is None: depths = {}
        depths[tree["node"]] = depth
        for child in tree.get("children", []):
            assign_depth(child, depth + 1, depths)
        return depths

    depths = assign_depth(data["tree"])
    for node_id, depth in depths.items():
        G.nodes[node_id]["subset"] = depth

    pos = nx.multipartite_layout(G, subset_key="subset", align="horizontal")
    max_y = max(p[1] for p in pos.values())
    pos = {k: (v[0], max_y - v[1]) for k, v in pos.items()}

    fig = go.Figure()

    for u, v in edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line={"width": 1.5, "color": colors["muted"]},
            showlegend=False, hoverinfo="skip",
        ))

    for node_info in nodes_list:
        nid = node_info["id"]
        status = node_info["status"]
        x, y = pos[nid]
        color_key = STATUS_COLORS.get(status, "muted")
        node_color = colors.get(color_key, color_key)
        fig.add_trace(go.Scatter(
            x=[x], y=[y], mode="markers+text",
            marker={"size": 30, "color": node_color, "line": {"width": 2, "color": "white"}},
            text=[nid], textposition="bottom center",
            textfont={"size": 11, "color": colors["text"]},
            showlegend=False, hovertext=f"{nid}: {status}",
        ))

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
