import unittest
from expense_tracker import get_expense, add_new_expense, expenses

class TestExpenseTracker(unittest.TestCase):

    def test_get_expense(self):
        self.assertEqual(get_expense("Pizza 30"), ("Pizza", 30.0))
        self.assertEqual(get_expense("Burger 15.5"), ("Burger", 15.5))
        self.assertEqual(get_expense("Coffee 5"), ("Coffee", 5.0))
        self.assertEqual(get_expense("Sandwich 7.25"), ("Sandwich", 7.25))

    def test_add_new_expense(self):
        self.assertTrue(add_new_expense("yes"))
        self.assertTrue(add_new_expense("Yes"))
        self.assertTrue(add_new_expense("y"))
        self.assertFalse(add_new_expense("no"))
        self.assertFalse(add_new_expense("No"))
        self.assertFalse(add_new_expense("n"))

    def test_expenses_initialization(self):
        self.assertEqual(expenses, {"Food": {}, "Entertainment": {}, "Transport": {}, "Housing": {}, "Healthcare": {}})

if __name__ == "__main__":
    unittest.main()
