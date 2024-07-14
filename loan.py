from datetime import datetime


class Loan:
    def __init__(self, loan_id, amount, interest_rate, term, start_date):
        # Initialize loan object with given parameters
        self.loan_id = loan_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.term = term
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = self.start_date.replace(year=self.start_date.year + term)
        self.monthly_payment = self.calculate_monthly_payment()

    def calculate_monthly_payment(self):
        # Calculate the monthly payment based on the loan details
        monthly_rate = self.interest_rate / 12 / 100
        payments = self.term * 12
        if monthly_rate == 0:
            return self.amount / payments
        return self.amount * monthly_rate / (1 - (1 + monthly_rate) ** -payments)
