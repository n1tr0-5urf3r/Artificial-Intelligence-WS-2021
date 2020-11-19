### ------------ (a) -------------- ###
class BinaryTree:

    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


### ------------ (b) -------------- ###
tree = BinaryTree(1,
                  BinaryTree(2,
                             BinaryTree(3,
                                        BinaryTree(4,
                                                   BinaryTree(5),
                                                   BinaryTree(6)),
                                        BinaryTree(7,
                                                   BinaryTree(8),
                                                   None)
                                        ), None),
                  BinaryTree(9,
                             BinaryTree(10,
                                        BinaryTree(11),
                                        BinaryTree(12)),
                             BinaryTree(13,
                                        BinaryTree(14,
                                                   BinaryTree(15),
                                                   BinaryTree(16)),
                                        BinaryTree(17, None, BinaryTree(18))))
                  )


### ------------ (c) -------------- ###
def search_tree(tree, val):
    """Actually a breadth first traversal of a tree

    !!!
    ASSUMING THE ROOT HAS A DEPTH OF 0
    !!!

    :param tree: The Binary Tree to be searched
    :type tree: BinaryTree() object
    :param val: The value to be searched for
    :type val: Int
    :return: The depth of the found value, or None if not found
    :rtype: Int or None
    """
    # Initialize values
    depth = 0
    # The queue is a list of tuples. Each tuple contains the subtree and depth so far
    queue = [(tree, depth)]
    while queue:
        tree = queue[0][0]
        depth = queue[0][1]
        # Using a queue of lists, as we dont want to use external libraries for this assignment
        if tree.value == val:
            return depth
        if tree.left:
            queue.append((tree.left, depth + 1))
        if tree.right:
            queue.append((tree.right, depth + 1))
        # Pop item from the queue
        queue = queue[1:]
    # Nothing found!
    return None

### ------------ (d) -------------- ###


def find_path(tree, val):
    """This is also a breadth first search 

    :param tree: The Binary Tree to be searched
    :type tree: BinaryTree() object
    :param val: The value to be searched for
    :type val: Int
    :return: A list of directions left/right
    :rtype: List of Strings or None
    """
    # The queue is a list of tuples. Each tuple contains the subtree and path so far
    queue = [(tree, [])]
    if tree.value == val:
        return "The searched value is the root!"

    while queue:
        tree = queue[0][0]

        # Using a queue of lists, as we dont want to use external libraries for this assignment
        if tree.value == val:
            return queue[0][1]
        if tree.left:
            # Need to copy the list, so we dont use a reference pointer of other subtrees
            path = queue[0][1].copy()
            path.append("left")
            queue.append((tree.left, path))
        if tree.right:
            path = queue[0][1].copy()
            path.append("right")
            queue.append((tree.right, path))
        # Pop item from the queue
        queue = queue[1:]
    # Nothing found!
    return None


values = [7, 8, 12, 15, 1, 9, 42]

for val in values:
    level = search_tree(tree, val)
    print('The value', val, 'is found in level', level)
    path = find_path(tree, val)
    print('The value', val, 'is found by taking the path', path)

### ------------------------------- ###

# Note: For parts (c) and (d), you can add input arguments but they must have default values. You can modify the code as you like but make sure each function can be called by the same name and input arguments as defined in the task.
