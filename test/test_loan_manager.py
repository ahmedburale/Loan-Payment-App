import unittest
from loan_manager import LoanManager
from loan import Loan


class TestLoanManager(unittest.TestCase):
    def setUp(self):
        # Set up a LoanManager with a test file
        self.loan_manager = LoanManager('test_loans.csv')

    def tearDown(self):
        # Clean up the test file after each test
        import os
        if os.path.exists('test_loans.csv'):
            os.remove('test_loans.csv')

    def test_add_loan(self):
        # Test adding a loan
        loan = Loan("1", 10000, 5, 5, "2022-01-01")
        self.loan_manager.add_loan(loan)
        self.assertEqual(len(self.loan_manager.get_loans()), 1)

    def test_edit_loan(self):
        # Test editing a loan
        loan = Loan("1", 10000, 5, 5, "2022-01-01")
        self.loan_manager.add_loan(loan)
        self.loan_manager.edit_loan("1", 12000, 4, 5, "2022-01-01")
        edited_loan = self.loan_manager.get_loan("1")
        self.assertEqual(edited_loan.amount, 12000)
        self.assertEqual(edited_loan.interest_rate, 4)

    def test_delete_loan(self):
        # Test deleting a loan
        loan = Loan("1", 10000, 5, 5, "2022-01-01")
        self.loan_manager.add_loan(loan)
        self.loan_manager.delete_loan("1")
        self.assertEqual(len(self.loan_manager.get_loans()), 0)

    def test_get_loan(self):
        # Test retrieving a loan
        loan = Loan("1", 10000, 5, 5, "2022-01-01")
        self.loan_manager.add_loan(loan)
        retrieved_loan = self.loan_manager.get_loan("1")
        self.assertIsNotNone(retrieved_loan)
        self.assertEqual(retrieved_loan.loan_id, "1")

    def test_get_loans(self):
        # Test retrieving all loans
        loan1 = Loan("1", 10000, 5, 5, "2022-01-01")
        loan2 = Loan("2", 15000, 4, 3, "2023-01-01")
        self.loan_manager.add_loan(loan1)
        self.loan_manager.add_loan(loan2)
        loans = self.loan_manager.get_loans()
        self.assertEqual(len(loans), 2)
        self.assertEqual(loans[0].loan_id, "1")
        self.assertEqual(loans[1].loan_id, "2")

    def test_load_loans_missing_columns(self):
        # Test loading loans from a CSV with missing columns
        with open('test_loans.csv', 'w') as f:
            f.write("Incorrect,Headers,Only\n")
        loan_manager = LoanManager('test_loans.csv')
        self.assertEqual(len(loan_manager.get_loans()), 0)


if __name__ == '__main__':
    unittest.main()
