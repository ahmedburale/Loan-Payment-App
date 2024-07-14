from datetime import datetime

import pandas as pd
from loan import Loan


class LoanManager:
    def __init__(self, filename='loans.csv'):
        # Initialize LoanManager with a CSV filename to store loan data
        self.filename = filename
        self.loans = self.load_loans()

    def load_loans(self):
        # Load loans from CSV file, if file not found or columns missing return an empty list
        try:
            df = pd.read_csv(self.filename)
            if 'Loan ID' in df.columns and 'Amount' in df.columns and 'Interest Rate' in df.columns and 'Term' in df.columns and 'Start Date' in df.columns:
                loans = [Loan(row['Loan ID'], row['Amount'], row['Interest Rate'], row['Term'], row['Start Date']) for _, row in df.iterrows()]
                return loans
            else:
                print("CSV file missing required columns")
                return []
        except FileNotFoundError:
            return []

    def save_loans(self):
        # Save the current loans to the CSV file
        df = pd.DataFrame([loan.__dict__ for loan in self.loans])
        df.to_csv(self.filename, index=False)

    def add_loan(self, loan):
        # Add a new loan to the list and save to the CSV file
        self.loans.append(loan)
        self.save_loans()

    def edit_loan(self, loan_id, amount, interest_rate, term, start_date):
        # Edit an existing loan based on loan_id and save changes
        for loan in self.loans:
            if loan.loan_id == loan_id:
                loan.amount = amount
                loan.interest_rate = interest_rate
                loan.term = term
                loan.start_date = datetime.strptime(start_date, '%Y-%m-%d')
                loan.end_date = loan.start_date.replace(year=loan.start_date.year + term)
                loan.monthly_payment = loan.calculate_monthly_payment()
                self.save_loans()
                return True
        return False

    def delete_loan(self, loan_id):
        # Delete a loan from the list based on loan_id and save changes
        self.loans = [loan for loan in self.loans if loan.loan_id != loan_id]
        self.save_loans()

    def get_loan(self, loan_id):
        # Retrieve a loan based on loan_id
        for loan in self.loans:
            if loan.loan_id == loan_id:
                return loan
        return None

    def get_loans(self):
        # Get all loans
        return self.loans
