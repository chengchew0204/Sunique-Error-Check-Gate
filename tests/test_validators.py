import unittest
from app.validators.base import ValidationResult, BaseValidator


class TestValidationResult(unittest.TestCase):
    """
    Test cases for ValidationResult class.
    """
    
    def test_validation_result_initialization(self):
        result = ValidationResult("Test Rule")
        self.assertEqual(result.rule_name, "Test Rule")
        self.assertTrue(result.passed)
        self.assertEqual(len(result.issues), 0)
        self.assertEqual(len(result.suggested_fixes), 0)
    
    def test_add_issue(self):
        result = ValidationResult("Test Rule")
        result.add_issue("Test issue", severity="error")
        
        self.assertFalse(result.passed)
        self.assertEqual(len(result.issues), 1)
        self.assertEqual(result.issues[0]['message'], "Test issue")
        self.assertEqual(result.issues[0]['severity'], "error")
    
    def test_add_suggested_fix(self):
        result = ValidationResult("Test Rule")
        result.add_suggested_fix("Fix this issue")
        
        self.assertEqual(len(result.suggested_fixes), 1)
        self.assertEqual(result.suggested_fixes[0], "Fix this issue")
    
    def test_to_dict(self):
        result = ValidationResult("Test Rule")
        result.add_issue("Issue 1")
        result.add_suggested_fix("Fix 1")
        
        result_dict = result.to_dict()
        
        self.assertEqual(result_dict['rule'], "Test Rule")
        self.assertFalse(result_dict['passed'])
        self.assertEqual(len(result_dict['issues']), 1)
        self.assertEqual(len(result_dict['suggested_fixes']), 1)


if __name__ == '__main__':
    unittest.main()

