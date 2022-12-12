def dls(node, depth):
    lethal = node.life_total <= 0
    if depth == 0:
        if lethal:
            return node, True
        else:
            return None, True
    elif depth > 0:
        any_remaining = False
        children = node.generate_children()
        for child in children:
            data, b = dls(child, depth-1)
            if data is not None:
                return data, True
            if b:
                any_remaining = True
        return None, any_remaining
    return None


class GameTree:
    def __init__(self, root):
        self.root = root

    def tree_search(self):
        max_depth = (self.root.life_total // 4) + 5
        for depth in range(max_depth+1):
            data, b, = dls(self.root, depth)
            if data is not None:
                return data
            elif not b:
                return None
        return None
