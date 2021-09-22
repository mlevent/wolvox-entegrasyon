from collections import defaultdict

class NodeTree:
    def __init__(self, nodes):
        self.nodes = nodes
        self.nodes_by_parent = defaultdict(list)

        for node in self.nodes:
            self.nodes_by_parent[node["parent_id"]].append(node)

    def visit_node(self, node, level=0, parent=None):
        yield (level, node, parent)
        for child in self.nodes_by_parent.get(node["id"], ()):
            yield from self.visit_node(child, level=level + 1, parent=node)

    def walk_tree(self):
        for node in self.root_nodes:
            yield from self.visit_node(node)

    @property
    def root_nodes(self):
        return self.nodes_by_parent.get(0, ())