class BSTNode:
    def __init__(self, key, value):
        self.key = key          # movie title (lowercase)
        self.value = value      # Movie object
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    # ================= INSERT =================
    def insert(self, key, value):
        if self.root is None:
            self.root = BSTNode(key, value)
        else:
            self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, value)
            else:
                self._insert(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, value)
            else:
                self._insert(node.right, key, value)
        else:
            # duplicate key → overwrite movie
            node.value = value

    # ================= SEARCH =================
    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    # ================= INORDER (OPTIONAL) =================
    def inorder(self):
        result = []

        def _dfs(node):
            if not node:
                return
            _dfs(node.left)
            result.append(node.value)
            _dfs(node.right)

        _dfs(self.root)
        return result
