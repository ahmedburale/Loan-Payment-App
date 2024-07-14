import unittest
from loan import Loan


class TestLoan(unittest.TestCase):
    def test_monthly_payment(self):
        # Test the monthly payment calculation
        loan = Loan("1", 10000, 5, 5, "2022-01-01")
        self.assertAlmostEqual(loan.calculate_monthly_payment(), 188.71, places=2)

    def test_monthly_payment_zero_interest(self):
        # Test monthly payment calculation with zero interest
        loan = Loan("2", 10000, 0, 5, "2022-01-01")
        self.assertAlmostEqual(loan.calculate_monthly_payment(), 166.67, places=2)

    def test_end_date_calculation(self):
        # Test the end date calculation
        loan = Loan("3", 10000, 5, 5, "2022-01-01")
        self.assertEqual(loan.end_date.strftime('%Y-%m-%d'), '2027-01-01')


if __name__ == '__main__':
    unittest.main()
