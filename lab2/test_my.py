import unittest
from main import LogicFunctionAnalyzer

class TestLogicFunctionAnalyzer(unittest.TestCase):
    
    def test_parse_function(self):
        analyzer = LogicFunctionAnalyzer()
        self.assertEqual(analyzer.parse_function("a->b"), "a <= b")
        self.assertEqual(analyzer.parse_function("a&b"), "a&b")
        self.assertEqual(analyzer.parse_function("a|b"), "a|b")
    
    def test_evaluate_function(self):
        analyzer = LogicFunctionAnalyzer()
        self.assertEqual(analyzer.evaluate_function("a & b", {"a": 1, "b": 0}), False)
        self.assertEqual(analyzer.evaluate_function("a & b", {"a": 1, "b": 1}), True)
        self.assertEqual(analyzer.evaluate_function("a | b", {"a": 0, "b": 1}), True)
    
    def test_build_truth_table(self):
        analyzer = LogicFunctionAnalyzer()
        analyzer.build_truth_table("a & b")
        expected_table = [
            [0, 0, 0],
            [0, 1, 0],
            [1, 0, 0],
            [1, 1, 1]
        ]
        self.assertEqual(analyzer.truth_table, expected_table)
    
    def test_get_minterms(self):
        analyzer = LogicFunctionAnalyzer()
        analyzer.build_truth_table("a & b")
        minterms = analyzer.get_minterms()
        self.assertEqual(minterms, [3])
    
    def test_get_maxterms(self):
        analyzer = LogicFunctionAnalyzer()
        analyzer.build_truth_table("a & b")
        maxterms = analyzer.get_maxterms()
        self.assertEqual(maxterms, [0, 1, 2])
    
    def test_get_index_form(self):
        analyzer = LogicFunctionAnalyzer()
        analyzer.build_truth_table("a & b")
        decimal, binary = analyzer.get_index_form()
        self.assertEqual(binary, "0001")
        self.assertEqual(decimal, 1)
    
    def test_build_sdnf(self):
        analyzer = LogicFunctionAnalyzer()
        analyzer.build_truth_table("a & b")
        sdnf, minterms = analyzer.build_sdnf()
        self.assertEqual(minterms, [3])
        self.assertIn("a", sdnf)
    
    def test_build_sknf(self):
        analyzer = LogicFunctionAnalyzer()
        analyzer.build_truth_table("a & b")
        sknf, maxterms = analyzer.build_sknf()
        self.assertEqual(maxterms, [0, 1, 2])
        self.assertIn("∨", sknf)
    
    def test_analyze_function(self):
        analyzer = LogicFunctionAnalyzer()
        try:
            analyzer.analyze_function("a & b")
            success = True
        except:
            success = False
        self.assertTrue(success)
    
    def test_single_variable(self):
        analyzer = LogicFunctionAnalyzer()
        analyzer.build_truth_table("a")
        expected_table = [
            [0, 0],
            [1, 1]
        ]
        self.assertEqual(analyzer.truth_table, expected_table)

if __name__ == "__main__":
    unittest.main()