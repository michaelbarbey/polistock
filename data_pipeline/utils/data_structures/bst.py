class BSTNode:
    def __init__(self, key, txn):
        # key function used for sorting parameter
        self.key   = key
        self.txns  = [txn]   # allows duplicates on same key
        self.left  = None
        self.right = None

class TransactionBST:
    def __init__(self, key_func):
        self.root     = None
        self.key_func = key_func

    def insert(self, txn):
        k = self.key_func(txn)
        if self.root is None:
            # first node in the tree
            self.root = BSTNode(k, txn)
        else:
            # walks tree to insert
            node = self.root
            while True:
                if k < node.key:
                    if node.left:
                        node = node.left
                        continue
                    node.left = BSTNode(k, txn)
                    break
                elif k > node.key:
                    if node.right:
                        node = node.right
                        continue
                    node.right = BSTNode(k, txn)
                    break
                else:
                    # same key appends to node list
                    node.txns.append(txn)
                    break

    def inorder(self, reverse=False): # if True returns descending order
        result = []
        def _traverse(node):
            if not node:
                return
            if not reverse:
                _traverse(node.left)
                for t in node.txns:
                    result.append(t)
                _traverse(node.right)
            else:
                _traverse(node.right)
                for t in node.txns:
                    result.append(t)
                _traverse(node.left)

        _traverse(self.root)
        return result #all transactions in order