import sqlite3

def initialize_database():
    """Create the rules table if it doesn't exist.

    This function is a one-time setup for the database. It
    creates a table named 'rules' with two columns: 'id' and
    'rule_string'. The 'id' column is an auto-incrementing
    primary key and the 'rule_string' column is where we store
    the actual rule strings.

    """
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rules (
                 id INTEGER PRIMARY KEY,
                 rule_string TEXT not null)''')
    conn.commit()
    conn.close()


def save_rule(rule_string):
    """
    Save a rule string to the database.

    If the rule string already exists in the database, do nothing.
    Otherwise, insert the rule string into the database.

    :param str rule_string: The rule string to save.
    :return: None
    """
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()

    # Check if the rule already exists
    c.execute("SELECT COUNT(*) FROM rules WHERE rule_string = ?", (rule_string,))
    result = c.fetchone()[0]

    if result == 0:  # If the rule doesn't exist, insert it
        c.execute("INSERT INTO rules (rule_string) VALUES (?)", (rule_string,))
        conn.commit()
        print("Rule inserted.")
    else:
        print("Rule already exists.")

    conn.close()


def load_rules():
    """
    Load all rule strings from the database.

    :return: A list of all rule strings in the database.
    :rtype: list[str]
    """
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()
    c.execute("SELECT rule_string FROM rules")
    rules = c.fetchall()
    conn.close()
    return [rule[0] for rule in rules]

def load_rule(rule_string):
    """
    Load a rule string from the database.

    If the rule string does not exist in the database, return None.
    Otherwise, return the rule string.

    :param str rule_string: The rule string to load.
    :return: The loaded rule string, or None if the rule string does not exist.
    :rtype: str or None
    """
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()
    c.execute("SELECT rule_string FROM rules WHERE rule_string=?", (rule_string,))
    rule = c.fetchone()
    conn.close()
    if rule is None:
        return None  # or raise a custom error
    return rule[0]

def delete_rule(rule_string):
    """
    Delete a rule string from the database.

    :param str rule_string: The rule string to delete.
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()
    c.execute("DELETE FROM rules WHERE rule_string=?", (rule_string,))
    conn.commit()
    conn.close()

def update_rule(old_rule_string, new_rule_string):
    """
    Update a rule string in the database.

    Replace the existing rule string with the new rule string. If the
    rule string does not exist in the database, do nothing.

    :param str old_rule_string: The existing rule string to update.
    :param str new_rule_string: The new rule string to update with.
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()
    c.execute("UPDATE rules SET rule_string=? WHERE rule_string=?", (new_rule_string, old_rule_string))
    conn.commit()
    conn.close()

def clear_rules():
    """
    Clear all rules from the database.

    This function will delete all rules from the database. It's mostly used for
    testing purposes.

    :return: None
    :rtype: None
    """
    conn = sqlite3.connect('rule_engine.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM rules")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    finally:
        conn.close()