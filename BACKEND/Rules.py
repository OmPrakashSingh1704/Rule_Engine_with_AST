from .Tokenizer import tokenize
from .AST import Node

def create_rule(rule_string):
    """
    Create an abstract syntax tree (AST) from a given rule string.

    This function implements the Shunting-yard algorithm to parse a
    rule string into an abstract syntax tree (AST). The AST is a tree
    of nodes, where each node represents either an operand (condition)
    or an operator (logical operation). The root of the tree is the
    top-level operator.

    :param rule_string: A string representing the rule to be parsed.
    :return: The root of the abstract syntax tree for the given rule.
    """
    tokens = tokenize(rule_string)

    precedence = {'OR': 1, 'AND': 2}
    output = []  # Operand stack
    operators = []  # Operator stack

    def pop_operator():
        # Pop an operator and create a node
        operator = operators.pop()
        right = output.pop()
        left = output.pop()
        output.append(Node("operator", left, right, operator))

    for token in tokens:
        if token == '(':
            operators.append(token)  # Push '(' to the stack
        elif token == ')':
            while operators[-1] != '(':
                pop_operator()
            operators.pop()  # Remove '('
        elif token in precedence:
            while (operators and operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[token]):
                pop_operator()
            operators.append(token)  # Push the current operator
        else:
            # Operand (condition), push it to output stack
            output.append(Node("operand", value=token))

    while operators:
        pop_operator()

    return output[0]  # The root of the AST


def combine_rules(rules):
    # Combine a list of ASTs using AND
    """
    Combine a list of abstract syntax trees (ASTs) into a single AST using logical AND.

    :param rules: A list of ASTs to be combined.
    :return: The root of the combined AST.
    """
    if not rules:
        return None

    # Start with the first rule
    combined_ast = rules[0]

    # Combine each subsequent rule with an AND node
    for rule in rules[1:]:
        combined_ast = Node("operator", combined_ast, rule, "AND")

    return combined_ast


def evaluate_rule(node, data):
    # Recursively evaluate the AST
    """
    Recursively evaluate the AST and return the result.

    Given a Node object representing the root of an abstract syntax tree (AST)
    and a dictionary of data, this function will evaluate the condition(s)
    represented by the AST against the data and return the result.

    :param node: The root of the AST to evaluate
    :param data: A dictionary of data to evaluate the condition(s) against
    :return: The result of evaluating the condition(s) against the data
    :rtype: bool
    """
    if node.operation == "operand":
        # Evaluate the condition in the context of the provided data
        # We use Python's eval function here to evaluate conditions like "age > 30"
        # e.g., it will evaluate "data['age'] > 30"
        try:
            return eval(node.value, {}, data)  # Evaluate condition with user data
        except Exception as e:
            print(f"Error evaluating condition: {node.value}. Error: {e}")
            return False

    elif node.operation == "operator":
        if node.value == "AND":
            # Return True if both left and right subtrees are True
            return evaluate_rule(node.left, data) and evaluate_rule(node.right, data)
        elif node.value == "OR":
            # Return True if either left or right subtree is True
            return evaluate_rule(node.left, data) or evaluate_rule(node.right, data)
