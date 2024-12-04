class Node:
    def __init__(self, depth=0, parent=None):
        self.depth = depth
        self.parent = parent
        self.children = []
    
    def is_regular_pair(self):
        return isinstance(self.children[0], int)\
            and isinstance(self.children[1], int)
    
    def is_left_child(self):
        return self.parent and self is self.parent.children[0]

    def add_child(self, child):
        self.children.append(child)
    
    def __str__(self):
        left, right = self.children
        return f'[{left},{right}]'

    def find_exploding_pair(self):
        if self.is_regular_pair():
            if self.depth >= 4:
                return self
        else:
            left, right = self.children
            ret = None
            if isinstance(left, Node):
                if not ret:
                    ret = left.find_exploding_pair()
            if isinstance(right, Node):
                if not ret:
                    ret = right.find_exploding_pair()
            return ret

    def find_regular_number_to_left(self):
        node = self
        while node and node.is_left_child():
            node = node.parent
        if not node:
            return None
        if isinstance(node.children[0], int):
            return (node, 0)
        node = node.children[0]
        while not node.is_regular_pair():
            node = node.children[1]
        return (node, 1)

def parse_snailfish_number(number):
    stack = []
    root = None
    for c in number:
        parent = None if not stack else stack[-1]
        if c.isdigit():
            digit = int(c)
            parent.add_child(digit)
        elif c == '[':
            node = Node(0 if parent is None else (parent.depth + 1), parent)
            stack.append(node)
            if parent:
                parent.add_child(node)
        elif c == ']':
            root = stack.pop()

    return root
