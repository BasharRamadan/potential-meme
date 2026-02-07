import networkx as nx


def build_dag():
    graph = nx.DiGraph()
    nodes = ["A", "B", "C", "D", "E"]
    graph.add_nodes_from(nodes)
    graph.add_edges_from(
        [
            ("A", "C"),
            ("B", "C"),
            ("C", "D"),
            ("C", "E"),
        ]
    )
    return graph


def save_dag_image(graph, output_path="dag.svg"):
    pos = {
        "A": (-1.0, 1.0),
        "B": (1.0, 1.0),
        "C": (0.0, 0.0),
        "D": (-1.0, -1.0),
        "E": (1.0, -1.0),
    }
    width, height = 600, 400
    scale_x, scale_y = 200, 140
    node_radius = 28
    node_color = "#CCE5FF"
    edge_color = "#333333"

    def to_svg_coords(point):
        x, y = point
        return (
            width / 2 + x * scale_x,
            height / 2 - y * scale_y,
        )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        "<defs>",
        '<marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" '
        'orient="auto" markerUnits="strokeWidth">',
        f'<polygon points="0 0, 10 3.5, 0 7" fill="{edge_color}" />',
        "</marker>",
        "</defs>",
    ]

    for source, target in graph.edges():
        x1, y1 = to_svg_coords(pos[source])
        x2, y2 = to_svg_coords(pos[target])
        lines.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{edge_color}" stroke-width="2" marker-end="url(#arrowhead)" />'
        )

    for node, point in pos.items():
        x, y = to_svg_coords(point)
        lines.append(
            f'<circle cx="{x}" cy="{y}" r="{node_radius}" '
            f'stroke="{edge_color}" stroke-width="2" fill="{node_color}" />'
        )
        lines.append(
            f'<text x="{x}" y="{y + 5}" text-anchor="middle" '
            'font-family="Arial, sans-serif" font-size="16" font-weight="bold">'
            f"{node}</text>"
        )

    lines.append("</svg>")
    with open(output_path, "w", encoding="utf-8") as file_handle:
        file_handle.write("\n".join(lines))


if __name__ == "__main__":
    dag = build_dag()
    save_dag_image(dag)
