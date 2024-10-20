class Node:
    def __init__(self, operation, left=None, right=None, value=None):
        """
        Initialize a Node object.

        :param operation: The operation of this node ("operator" or "operand")
        :param left: The left child of this node (another Node)
        :param right: The right child of this node (another Node)
        :param value: The value of this node (for operand nodes)
        """
        self.operation = operation  # "operator" or "operand"
        self.left = left  # Left child (another Node)
        self.right = right  # Right child (another Node)
        self.value = value  # For operand nodes (e.g., age > 30)

    def __repr__(self):
        """
        Return a string representation of the Node object.

        This representation is a string of the form:
        `Node(type=OPERATION, left=LEFT, right=RIGHT, value=VALUE)`

        :return: A string representation of the Node object
        :rtype: str
        """
        return f"Node(type={self.operation}, left={self.left}, right={self.right}, value={self.value})"

    def __eq__(self, other):
        # Check if other is an instance of Node
        """
        Check if two Node objects are equal.

        Two Node objects are equal if and only if all of their attributes are equal.

        :param other: The other Node object to compare to
        :return: True if the two Node objects are equal, False otherwise
        :rtype: bool
        """
        if not isinstance(other, Node):
            return False

        # Compare attributes for equality
        return (self.operation == other.operation and
                self.value == other.value and
                self.left == other.left and
                self.right == other.right)
