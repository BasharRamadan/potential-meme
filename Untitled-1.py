from __future__ import annotations

from typing import Dict, Tuple

import networkx as nx


NodePosition = Dict[str, Tuple[float, float]]


def create_dag() -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_edges_from(
        [
            ("A", "C"),
            ("B", "C"),
            ("C", "D"),
            ("C", "E"),
        ]
    )
    return graph


def svg_arrow(marker_id: str) -> str:
    return "\n".join(
        [
            f'<marker id="{marker_id}" markerWidth="10" markerHeight="7" '
            'refX="10" refY="3.5" orient="auto" markerUnits="strokeWidth" '
            'viewBox="0 0 10 7">',
            '<polygon points="0 0, 10 3.5, 0 7" fill="#1F77B4" />',
            "</marker>",
        ]
    )


def render_svg(graph: nx.DiGraph, positions: NodePosition, output_path: str) -> None:
    width, height = 600, 400
    radius = 32
    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        "<defs>",
        svg_arrow("arrow"),
        "</defs>",
        '<rect width="100%" height="100%" fill="white" />',
    ]

    def to_canvas(pos: Tuple[float, float]) -> Tuple[float, float]:
        x, y = pos
        return (
            width * (0.5 + x * 0.35),
            height * (0.5 - y * 0.35),
        )

    for source, target in graph.edges:
        x1, y1 = to_canvas(positions[source])
        x2, y2 = to_canvas(positions[target])
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2) ** 0.5
        if length:
            offset_x = dx / length * radius
            offset_y = dy / length * radius
        else:
            offset_x = 0.0
            offset_y = 0.0
        svg_lines.append(
            "".join(
                [
                    f'<line x1="{x1 + offset_x}" y1="{y1 + offset_y}" '
                    f'x2="{x2 - offset_x}" y2="{y2 - offset_y}" ',
                    'stroke="#1F77B4" stroke-width="2" marker-end="url(#arrow)" />',
                ]
            )
        )

    for node, pos in positions.items():
        x, y = to_canvas(pos)
        svg_lines.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="#E6F2FF" '
            'stroke="#1F77B4" stroke-width="2" />'
        )
        svg_lines.append(
            f'<text x="{x}" y="{y + 5}" text-anchor="middle" '
            'font-family="Arial" font-size="16" fill="#1F2933">'
            f"{node}</text>"
        )

    svg_lines.append("</svg>")

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(svg_lines))


def main() -> None:
    graph = create_dag()
    positions = {
        "A": (-1.0, 1.0),
        "B": (1.0, 1.0),
        "C": (0.0, 0.0),
        "D": (-1.0, -1.0),
        "E": (1.0, -1.0),
    }
    render_svg(graph, positions, "dag.svg")


if __name__ == "__main__":
    main()
