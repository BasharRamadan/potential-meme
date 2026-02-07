class DiGraph:
    def __init__(self) -> None:
        self._edges = []
        self._nodes = set()

    def add_edges_from(self, edges):
        for source, target in edges:
            self._edges.append((source, target))
            self._nodes.add(source)
            self._nodes.add(target)

    @property
    def edges(self):
        return list(self._edges)

    @property
    def nodes(self):
        return list(self._nodes)
