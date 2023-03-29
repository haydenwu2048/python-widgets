import networkx as nx
import matplotlib.pyplot as plt


def parse_markdown_list(markdown_list):
    tree = {}
    stack = []

    for line in markdown_list:
        level = line.count("  ")
        node = line.strip().lstrip("-").strip()
        stack = stack[:level]
        stack.append(node)

        if node not in tree:
            tree[node] = []

        if level > 0:
            parent = stack[-2]
            tree[parent].append(node)

    return tree


def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed={}):
        if pos is None:
            pos = {}
        if root not in parsed:
            parsed[root] = None
            neighbors = list(G.neighbors(root))
            if len(neighbors) != 0:
                dx = width / len(neighbors)
                nextx = xcenter - width / 2 - dx / 2
                for neighbor in neighbors:
                    nextx += dx
                    pos = _hierarchy_pos(G, neighbor, width=dx, vert_gap=vert_gap, vert_loc=vert_loc - vert_gap,
                                         xcenter=nextx, pos=pos, parent=root, parsed=parsed)
            pos[root] = (xcenter, vert_loc)
        return pos

    pos = _hierarchy_pos(G, root, width=width, vert_gap=vert_gap, vert_loc=vert_loc, xcenter=xcenter)
    return pos


def create_mind_map(tree, root):
    G = nx.DiGraph()

    for parent, children in tree.items():
        G.add_node(parent)
        for child in children:
            G.add_node(child)
            G.add_edge(parent, child)

    pos = hierarchy_pos(G, root)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, font_size=12, font_weight='bold', node_color='skyblue',
            edge_color='gray')
    plt.show()


markdown_list = [
    "- Root",
    "  - child 1",
    "    - grandchild 1",
    "    - grandchild 2",
    "    - grandchild 3",
    "  - child 2",
]

tree = parse_markdown_list(markdown_list)
print(tree)
root = "Root"
create_mind_map(tree, root)
