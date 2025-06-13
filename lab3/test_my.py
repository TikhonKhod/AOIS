import unittest
from main1 import *
import io
import sys

class TestAllFunctions(unittest.TestCase):
    def setUp(self):
        # Перехватываем вывод для тестов с печатью
        self.held_stdout = io.StringIO()
        sys.stdout = self.held_stdout
    
    def tearDown(self):
        sys.stdout = sys.__stdout__

    # Тесты для validate_expr
    def test_validate_expr_valid(self):
        self.assertTrue(validate_expr("a & b | !c"))
        self.assertTrue(validate_expr("a->b"))
        self.assertTrue(validate_expr("a ~ b"))
        self.assertTrue(validate_expr("((a|b)&(c->d))~e"))
    
    def test_validate_expr_invalid(self):
        self.assertFalse(validate_expr("a ^ b"))
        self.assertFalse(validate_expr("a && b"))
        self.assertFalse(validate_expr("a | b | f"))
        self.assertFalse(validate_expr("a ->> b"))
        self.assertFalse(validate_expr("a @ b"))

    # Тесты для expr_to_python
    def test_expr_to_python_implication(self):
        self.assertEqual(expr_to_python("a->b"), "(not a or b)")
        self.assertEqual(expr_to_python("!a->b"), "(not not a or b)")
    
    def test_expr_to_python_equivalence(self):
        self.assertEqual(expr_to_python("a~b"), "((a) == (b))")
        self.assertEqual(expr_to_python("a~!b"), "((a) == (not b))")
    
    def test_expr_to_python_operators(self):
        self.assertEqual(expr_to_python("!a & b"), "not a and b")
        self.assertEqual(expr_to_python("a | b"), "a or b")

    # Тесты для truth_table_builder
    def test_truth_table_builder_2_vars(self):
        vars_list = ['a', 'b']
        table, minterms, maxterms = truth_table_builder(vars_list, "a & b")
        self.assertEqual(len(table), 4)
        self.assertEqual(len(minterms), 1)
        self.assertEqual(len(maxterms), 3)
    
    def test_truth_table_builder_3_vars(self):
        vars_list = ['a', 'b', 'c']
        table, minterms, maxterms = truth_table_builder(vars_list, "a & b | c")
        self.assertEqual(len(table), 8)
        self.assertTrue(len(minterms) > 0)
        self.assertTrue(len(maxterms) > 0)
    
    def test_truth_table_builder_errors(self):
        with self.assertRaises(ValueError):
            truth_table_builder(['a', 'b'], "a && b")
        with self.assertRaises(ValueError):
            truth_table_builder([], "a & b")

    # Тесты для find_differences
    def test_find_differences(self):
        self.assertEqual(find_differences((0, 0), (0, 1)), (True, 1))
        self.assertEqual(find_differences((1, 0), (1, 1)), (True, 1))
        self.assertEqual(find_differences((1, 0), (0, 1)), (False, -1))
        self.assertEqual(find_differences((1, 0, 1), (1, 0, 0)), (True, 2))

    # Тесты для combine_terms
    def test_combine_terms(self):
        terms = [(0, 0), (0, 1)]
        result = combine_terms(terms)
        self.assertEqual(result, [(0, 'X')])
        
        terms = [(0, 0), (1, 1)]
        result = combine_terms(terms)
        self.assertEqual(len(result), 2)
        
        terms = [(1, 0, 0), (1, 0, 1)]
        result = combine_terms(terms)
        self.assertEqual(result, [(1, 0, 'X')])

    # Тесты для format_term
    def test_format_term_dnf(self):
        vars_list = ['a', 'b']
        self.assertEqual(format_term((1, 0), vars_list, True), "a & ¬b")
        self.assertEqual(format_term((0, 'X'), vars_list, False), "¬a ∨ x")
        self.assertEqual(format_term(('X', 1), vars_list, True), "b")
        self.assertEqual(format_term((1, 0, 1), ['a', 'b', 'c'], True), "a & ¬b & c")

    def test_format_term_cnf(self):
        vars_list = ['a', 'b']
        self.assertEqual(format_term((1, 0), vars_list, False), "¬a ∨ b")
        self.assertEqual(format_term((0, 1), vars_list, False), "a ∨ ¬b")

    # Тесты для minimize_with_steps
    def test_minimize_with_steps_dnf(self):
        result = minimize_with_steps("a & b | a & !b", ['a', 'b'], True)
        self.assertEqual(len(result), 1)
        self.assertEqual(format_term(result[0], ['a', 'b'], True), "a")
    
    def test_minimize_with_steps_cnf(self):
        result = minimize_with_steps("(!a | b) & (a | !b)", ['a', 'b'], False)
        self.assertEqual(len(result), 1)
        self.assertEqual(format_term(result[0], ['a', 'b'], False), "¬a ∨ ¬b")

    # Тесты для minimize_with_table
    def test_minimize_with_table_dnf(self):
        result = minimize_with_table("a & b | a & !b", ['a', 'b'], True)
        self.assertEqual(len(result), 1)
        self.assertEqual(format_term(result[0], ['a', 'b'], True), "a")
    
    def test_minimize_with_table_cnf(self):
        result = minimize_with_table("(!a | b) & (a | !b)", ['a', 'b'], False)
        self.assertEqual(len(result), 1)
        self.assertEqual(format_term(result[0], ['a', 'b'], False), "¬a ∨ ¬b")

    # Тесты для create_karnaugh_map
    def test_create_karnaugh_map_2_vars(self):
        table = [((0,0), False), ((0,1), True), ((1,0), True), ((1,1), True)]
        create_karnaugh_map(table, ['a', 'b'])
        self.assertTrue(len(self.held_stdout.getvalue()) > 0)
        
    def test_create_karnaugh_map_3_vars(self):
        table = [((0,0,0), False), ((0,0,1), True), ((0,1,0), False), ((0,1,1), True),
                 ((1,0,0), True), ((1,0,1), True), ((1,1,0), True), ((1,1,1), True)]
        create_karnaugh_map(table, ['a', 'b', 'c'])
        self.assertTrue(len(self.held_stdout.getvalue()) > 0)
    
    def test_create_karnaugh_map_4_vars(self):
        table = [tuple(combo + (False,)) for combo in itertools.product([0,1], repeat=4)]
        create_karnaugh_map(table, ['a', 'b', 'c', 'd'])
        self.assertTrue(len(self.held_stdout.getvalue()) > 0)
    
    def test_create_karnaugh_map_invalid_vars(self):
        with self.assertRaises(ValueError):
            create_karnaugh_map([], ['a'])  # Менее 2 переменных

    # Тесты для simplify_cnf
    def test_simplify_cnf(self):
        terms = simplify_cnf("(!a | b) & (!a | !b) & (a | b)", ['a', 'b'])
        self.assertEqual(len(terms), 2)
        self.assertIn(tuple([0, 0]), terms)
        self.assertIn(tuple([0, 1]), terms)

    # Тесты для kmap_generator
    def test_kmap_generator(self):
        table, _, _ = truth_table_builder(['a', 'b'], "a & b")
        result = kmap_generator(table, ['a', 'b'])
        self.assertEqual(result, [])

    # Тесты для term_to_str
    def test_term_to_str(self):
        self.assertEqual(term_to_str((1, 0), ['a', 'b']), "a & ¬b")
        self.assertEqual(term_to_str(('X', 1), ['a', 'b']), "b")
        self.assertEqual(term_to_str((0, 'X'), ['a', 'b'], False), "¬a ∨ x")

    # Тесты для других функций
    def test_simplify_dnf(self):
        result = simplify_dnf("a & b | a & !b", ['a', 'b'])
        self.assertEqual(len(result), 1)
        self.assertEqual(format_term(result[0], ['a', 'b'], True), "a")

    def test_minimize_karnaugh_dnf(self):
        result = minimize_karnaugh_dnf("a & b", ['a', 'b'])
        self.assertEqual(result, [])

    def test_minimize_karnaugh_cnf(self):
        result = minimize_karnaugh_cnf("a & b", ['a', 'b'])
        self.assertEqual(result, [])

    # Тесты для обработки ошибок
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            truth_table_builder(['a', 'b'], "a && b")
        
        with self.assertRaises(ValueError):
            truth_table_builder([], "a & b")
        
        with self.assertRaises(ValueError):
            expr_to_python("a @@ b")

if __name__ == '__main__':
    unittest.main()