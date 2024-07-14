import unittest
from loan_app import LoanApp


class TestLoanApp(unittest.TestCase):
    def setUp(self):
        # Set up a LoanApp instance
        self.app = LoanApp()

    def test_validate_inputs_success(self):
        # Test successful validation of inputs
        self.app.loan_id.insert(0, "1")
        self.app.amount.insert(0, "10000")
        self.app.interest_rate.insert(0, "5")
        self.app.term.insert(0, "5")
        self.app.start_date.insert(0, "2022-01-01")
        self.assertTrue(self.app.validate_inputs())

    def test_validate_inputs_invalid_amount(self):
        # Test validation of inputs with an invalid amount
        self.app.loan_id.insert(0, "1")
        self.app.amount.insert(0, "abc")
        self.app.interest_rate.insert(0, "5")
        self.app.term.insert(0, "5")
        self.app.start_date.insert(0, "2022-01-01")
        self.assertFalse(self.app.validate_inputs())

    def test_validate_inputs_invalid_interest_rate(self):
        # Test validation of inputs with an invalid interest rate
        self.app.loan_id.insert(0, "1")
        self.app.amount.insert(0, "10000")
        self.app.interest_rate.insert(0, "xyz")
        self.app.term.insert(0, "5")
        self.app.start_date.insert(0, "2022-01-01")
        self.assertFalse(self.app.validate_inputs())

    def test_validate_inputs_invalid_term(self):
        # Test validation of inputs with an invalid term
        self.app.loan_id.insert(0, "1")
        self.app.amount.insert(0, "10000")
        self.app.interest_rate.insert(0, "5")
        self.app.term.insert(0, "term")
        self.app.start_date.insert(0, "2022-01-01")
        self.assertFalse(self.app.validate_inputs())

    def test_validate_inputs_invalid_start_date(self):
        # Test validation of inputs with an invalid start date
        self.app.loan_id.insert(0, "1")
        self.app.amount.insert(0, "10000")
        self.app.interest_rate.insert(0, "5")
        self.app.term.insert(0, "5")
        self.app.start_date.insert(0, "01-01-2022")
        self.assertFalse(self.app.validate_inputs())


if __name__ == '__main__':
    unittest.main()
