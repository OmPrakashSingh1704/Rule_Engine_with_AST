# Rule Engine with AST

## Overview

Rule Engine with AST is a customizable Python-based engine that parses and evaluates complex logical expressions using Abstract Syntax Trees (AST). It is designed to allow users to dynamically create, validate, and execute rules involving conditions, logical operators (AND, OR), and parentheses. This engine can be used for tasks such as data filtering, business logic validation, and decision-making automation.

## Features

- **Supports Complex Logical Expressions**: Handles conditions, logical operators (AND, OR), and nested parentheses.
- **Dynamic Rule Creation**: Define rules with conditions like "age > 30" or "department == 'Sales'".
- **Rule Validation**: Checks the syntax of rules, ensuring logical consistency (e.g., balanced parentheses, valid conditions).
- **Customizable Condition Handling**: Extendable for more complex types of conditions and operators.
- **Tokenization & Parsing**: Converts string-based rules into tokenized representations for easier processing.

## Requirements

- Python 3.6+
- Required packages can be found in `requirements.txt`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OmPrakashSingh1704/Rule_Engine_with_AST.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Rule_Engine_with_AST
   ```

3. Create virtual environment and activate it:

   ```bash
   python3 -m venv venv
   venv\Scripts\activate
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run application:

   ```bash
   ./bash.sh
   ```

## Usage

### Example Rule

```python
valid_rule_string = "(department == 'AI' AND age > 40 AND salary > 50000 AND prior_years_experience < 5)"
```

### Basic Workflow

1. **Tokenization**: Break down the rule into individual tokens.
2. **Validation**: Validate the syntax of the rule, ensuring conditions and operators are correctly used.
3. **Execution**: Apply the rule to your data to evaluate results.

### Code Example

```python
from rule_engine import is_valid_rule

rule_string = "(department == 'AI' AND age > 40 AND salary > 50000)"
is_valid, message = is_valid_rule(rule_string)

if is_valid:
    print("Rule is valid")
else:
    print(f"Rule is invalid: {message}")
```

## Testing

To run the unit tests:

```bash
python -m unittest discover tests
```

## Contact

For any queries, feel free to contact [Om Prakash Singh](mailto:thakur.omprakashsingh1704@gmail.com).
