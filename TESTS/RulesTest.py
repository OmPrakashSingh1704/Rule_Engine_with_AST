import unittest
from BACKEND.Rules import create_rule, evaluate_rule, combine_rules
from BACKEND.AST import Node
from BACKEND.db import initialize_database, save_rule, load_rules,load_rule,delete_rule,update_rule,clear_rules
from BACKEND.Tokenizer import is_valid_rule

rule_string1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience >5)"
rule_string2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
invalid_rule_string = "((age > 30 AND department => 'Marketing') AND (salary > 20000 OR experience > 5)"
valid_rule_string="(department = 'AI' AND age > 40 AND salary > 50000 AND prior_years_experience < 5)"

initialize_database()

class AST_TEST(unittest.TestCase):
    def test_create_rule(self):
        """
        Test that the create_rule function returns an AST Node.
        """
        ast_root = create_rule(rule_string1)
        self.assertEqual(type(ast_root), Node)
        ast_root = create_rule(rule_string1)
        self.assertEqual(type(ast_root), Node)

    def test_combine_rules(self):
        """
        Test that the combine_rules function combines two ASTs into one.
        :return:
        """
        ast_root1 = create_rule(rule_string1)
        ast_root2 = create_rule(rule_string2)
        ast_root=combine_rules([ast_root1, ast_root2])
        self.assertEqual(type(ast_root), Node)

    def test_evaluate_rule_True(self):
        """
        Test that the evaluate_rule function evaluates a rule to True when given the appropriate data.
        """
        ast_root = create_rule(rule_string1)
        self.assertTrue(evaluate_rule(ast_root, {"age": 35,"department": "Sales", "salary": 60000, "experience": 3}))

    def test_evaluate_rule_False(self):
        """
        Test that the evaluate_rule function evaluates a rule to False when given the appropriate data.
        """
        ast_root = create_rule(rule_string2)
        self.assertFalse(evaluate_rule(ast_root, {"age": 35,"department": "Sales", "salary": 60000, "experience": 3}))

    def test_db_save_rule_and_load_rules(self):
        """
        Test that the save_rule and load_rules functions work correctly.
        """
        ast_root1 = create_rule(rule_string1)
        ast_root2 = create_rule(rule_string2)
        ast_root=combine_rules([ast_root1, ast_root2])
        save_rule(rule_string1+" AND "+rule_string2)
        all_rules=load_rules()
        self.assertIn(rule_string1+" AND "+rule_string2, all_rules)


    def test_db_save_rule_and_load_rule(self):
        """
        Test that the save_rule and load_rule functions work correctly.
        :return:
        """
        ast_root1 = create_rule(rule_string1)
        ast_root2 = create_rule(rule_string2)
        ast_root=combine_rules([ast_root1, ast_root2])
        save_rule(rule_string1+" AND "+rule_string2)
        rule=load_rule(rule_string1+" AND "+rule_string2)
        self.assertIsNotNone(rule, "Rule not found in the database.")
        self.assertEqual(rule, rule_string1+" AND "+rule_string2)

    def test_db_delete_rule(self):
        """
        Test that the delete_rule function deletes a rule from the database.
        """
        ast_root1 = create_rule(rule_string1)
        ast_root2 = create_rule(rule_string2)
        ast_root=combine_rules([ast_root1, ast_root2])
        save_rule(rule_string1+" AND "+rule_string2)
        delete_rule(rule_string1+" AND "+rule_string2)
        all_rules=load_rules()
        self.assertNotIn(rule_string1+" AND "+rule_string2, all_rules)

    def test_db_update_rule(self):
        """
        Test that the update_rule function updates a rule in the database.
        :return:
        """
        ast_root1 = create_rule(rule_string1)
        ast_root2 = create_rule(rule_string2)
        ast_root=combine_rules([ast_root1, ast_root2])
        save_rule(rule_string1+" AND "+rule_string2)
        update_rule(rule_string1+" AND "+rule_string2, rule_string1+" OR "+rule_string2)
        rule=load_rule(rule_string1+" OR "+rule_string2)
        self.assertIsNotNone(rule, "Rule not found in the database.")
        self.assertEqual(rule, rule_string1+" OR "+rule_string2)

    def test_db_clear_rules(self):
        """
        Test that the clear_rules function clears all rules from the database.
        :return:
        """
        ast_root = create_rule(rule_string1)
        save_rule(rule_string1+" AND "+rule_string2)
        clear_rules()
        all_rules=load_rules()
        self.assertEqual(all_rules, [])

    def test_is_valid_rule_False(self):
        """
        Test that the is_valid_rule function returns False when given an invalid rule string.
        """
        self.assertFalse(is_valid_rule(invalid_rule_string)[0])

    def test_is_valid_rule_True(self):
        """
        Test that the is_valid_rule function returns True when given a valid rule string.
        """
        self.assertTrue(is_valid_rule(valid_rule_string)[0])

if __name__ == '__main__':
    unittest.main()
