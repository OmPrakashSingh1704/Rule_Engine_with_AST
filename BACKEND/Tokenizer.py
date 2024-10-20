import re

def is_valid_rule(rule_string):
    # 1. Check for balanced parentheses
    """
    Validate a rule string by checking for balanced parentheses and valid tokens.

    :param rule_string: The rule string to validate
    :return: A tuple of (True, "The rule is valid.") or (False, "Error message")

    >>> is_valid_rule("((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience >5)")
    (True, 'The rule is valid.')
    """
    if not is_parentheses_balanced(rule_string):
        return False, "Parentheses are not balanced."

    # 2. Tokenize the rule string
    tokens = tokenize(rule_string)

    # 3. Validate each token
    for token in tokens:
        if token in ('AND', 'OR', '(', ')'):
            # Logical operators and parentheses are valid tokens
            continue
        elif not is_valid_condition(token):
            return False, f"Invalid condition: {token}"

    return True, "The rule is valid."


def is_parentheses_balanced(rule_string):
    """Check if parentheses in the rule string are balanced."""
    stack = []
    for char in rule_string:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0


def is_valid_condition(condition):
    """Check if the condition is valid (e.g., age > 30, department == 'Sales')."""
    # Define a regex pattern for valid conditions
    # Updated pattern to include underscores in variable names
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*\s*(==|!=|>|<|>=|<=)\s*[a-zA-Z0-9'_]+$"

    # Check if the condition matches the pattern
    return bool(re.match(pattern, condition))


def replace_equals(input_string):
    """Replace '=' with '==' in conditions while avoiding '>=', '<=', '!='."""
    try:
        # This regex finds '=' that is not part of '>=', '<=', or '!=' and replaces it with '=='
        # Handles multiple spaces around '=' by capturing optional spaces
        return re.sub(r'(?<![><!=])\s*=\s*(?!=)', ' == ', input_string)
    except:
        return input_string


def tokenize(rule_string):
    # Replace single '=' with '=='
    """
    Tokenize a rule string into conditions, logical operators, and parentheses.

    :param rule_string: The rule string to tokenize
    :return: A list of tokens
    """
    rule_string = replace_equals(rule_string)

    # Use a regex pattern to split the rule string into tokens (conditions, logical operators, and parentheses)
    tokens = re.findall(r"\(|\)|AND|OR|[a-zA-Z_][a-zA-Z0-9_]*\s*(?:==|!=|>|<|>=|<=)\s*[a-zA-Z0-9'_]+", rule_string)

    # Remove any extraneous whitespace from tokens
    tokens = [token.strip() for token in tokens if token.strip()]

    return tokens
