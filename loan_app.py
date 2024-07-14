import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd

from loan_manager import LoanManager
from loan import Loan
import matplotlib.pyplot as plt
from datetime import datetime


class LoanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Loan Payment Tracker")
        self.geometry("800x600")

        # Initialize LoanManager
        self.loan_manager = LoanManager()

        # Configure styles for the widgets
        self.style = ttk.Style(self)
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 12), padding=10)
        self.style.configure('TEntry', font=('Helvetica', 12), padding=10)

        # Create menu and widgets
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        # Create the menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Add File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Loan", command=self.add_loan_window)
        file_menu.add_command(label="View Loans", command=self.view_loans)
        file_menu.add_command(label="Export to Excel", command=self.export_to_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def create_widgets(self):
        # Create and place the widgets for loan input
        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Loan ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.loan_id = ttk.Entry(frame)
        self.loan_id.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

        ttk.Label(frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount = ttk.Entry(frame)
        self.amount.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E)

        ttk.Label(frame, text="Interest Rate:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.interest_rate = ttk.Entry(frame)
        self.interest_rate.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)

        ttk.Label(frame, text="Term (Years):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.term = ttk.Entry(frame)
        self.term.grid(row=3, column=1, padx=5, pady=5, sticky=tk.E)

        ttk.Label(frame, text="Start Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_date = ttk.Entry(frame)
        self.start_date.grid(row=4, column=1, padx=5, pady=5, sticky=tk.E)

        # Create and place buttons for loan operations
        btn_frame = ttk.Frame(self, padding="10")
        btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.add_loan_btn = ttk.Button(btn_frame, text="Add Loan", command=self.add_loan)
        self.add_loan_btn.grid(row=0, column=0, padx=10, pady=10)

        self.view_loans_btn = ttk.Button(btn_frame, text="View Loans", command=self.view_loans)
        self.view_loans_btn.grid(row=0, column=1, padx=10, pady=10)

        self.plot_insights_btn = ttk.Button(btn_frame, text="Plot Insights", command=self.plot_insights)
        self.plot_insights_btn.grid(row=0, column=2, padx=10, pady=10)

        self.edit_loan_btn = ttk.Button(btn_frame, text="Edit Loan", command=self.edit_loan)
        self.edit_loan_btn.grid(row=0, column=3, padx=10, pady=10)

        self.delete_loan_btn = ttk.Button(btn_frame, text="Delete Loan", command=self.delete_loan)
        self.delete_loan_btn.grid(row=0, column=4, padx=10, pady=10)

        self.summary_btn = ttk.Button(btn_frame, text="Generate Summary", command=self.generate_summary)
        self.summary_btn.grid(row=0, column=5, padx=10, pady=10)

    def add_loan_window(self):
        # Clear input fields and prepare to add a new loan
        self.clear_entries()
        self.add_loan_btn.config(text="Add Loan", command=self.add_loan)

    def validate_inputs(self):
        # Validate all user inputs
        if not self.loan_id.get().strip():
            messagebox.showerror("Error", "Loan ID is required!")
            return False
        try:
            float(self.amount.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return False
        try:
            float(self.interest_rate.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Interest Rate must be a number!")
            return False
        if not self.term.get().strip().isdigit():
            messagebox.showerror("Error", "Term must be a number!")
            return False
        try:
            datetime.strptime(self.start_date.get().strip(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Start Date must be in YYYY-MM-DD format!")
            return False
        return True

    def add_loan(self):
        # Add a new loan if inputs are valid
        if not self.validate_inputs():
            return

        loan_id = self.loan_id.get().strip()
        amount = float(self.amount.get().strip())
        interest_rate = float(self.interest_rate.get().strip())
        term = int(self.term.get().strip())
        start_date = self.start_date.get().strip()

        loan = Loan(loan_id, amount, interest_rate, term, start_date)
        self.loan_manager.add_loan(loan)

        messagebox.showinfo("Success", "Loan added successfully!")
        self.clear_entries()

    def clear_entries(self):
        # Clear all input fields
        self.loan_id.delete(0, tk.END)
        self.amount.delete(0, tk.END)
        self.interest_rate.delete(0, tk.END)
        self.term.delete(0, tk.END)
        self.start_date.delete(0, tk.END)

    def view_loans(self):
        # Display all loans in a new window
        loans = self.loan_manager.get_loans()
        if not loans:
            messagebox.showerror("Error", "No loans found!")
            return

        view_window = tk.Toplevel(self)
        view_window.title("View Loans")

        tree = ttk.Treeview(view_window, columns=(
        "Loan ID", "Amount", "Interest Rate", "Term", "Start Date", "End Date", "Monthly Payment"), show="headings")
        tree.heading("Loan ID", text="Loan ID")
        tree.heading("Amount", text="Amount")
        tree.heading("Interest Rate", text="Interest Rate")
        tree.heading("Term", text="Term")
        tree.heading("Start Date", text="Start Date")
        tree.heading("End Date", text="End Date")
        tree.heading("Monthly Payment", text="Monthly Payment")

        for loan in loans:
            tree.insert("", tk.END, values=(
            loan.loan_id, loan.amount, loan.interest_rate, loan.term, loan.start_date.strftime('%Y-%m-%d'),
            loan.end_date.strftime('%Y-%m-%d'), f"{loan.monthly_payment:.2f}"))

        tree.pack(expand=True, fill=tk.BOTH)

    def edit_loan(self):
        # Edit an existing loan based on loan_id
        loan_id = self.loan_id.get().strip()
        loan = self.loan_manager.get_loan(loan_id)
        if not loan:
            messagebox.showerror("Error", "Loan ID not found!")
            return

        self.amount.delete(0, tk.END)
        self.amount.insert(0, loan.amount)
        self.interest_rate.delete(0, tk.END)
        self.interest_rate.insert(0, loan.interest_rate)
        self.term.delete(0, tk.END)
        self.term.insert(0, loan.term)
        self.start_date.delete(0, tk.END)
        self.start_date.insert(0, loan.start_date.strftime('%Y-%m-%d'))

        self.add_loan_btn.config(text="Update Loan", command=self.update_loan)

    def update_loan(self):
        # Update loan details if inputs are valid
        if not self.validate_inputs():
            return

        loan_id = self.loan_id.get().strip()
        amount = float(self.amount.get().strip())
        interest_rate = float(self.interest_rate.get().strip())
        term = int(self.term.get().strip())
        start_date = self.start_date.get().strip()

        success = self.loan_manager.edit_loan(loan_id, amount, interest_rate, term, start_date)
        if success:
            messagebox.showinfo("Success", "Loan updated successfully!")
            self.add_loan_btn.config(text="Add Loan", command=self.add_loan)
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Loan ID not found!")

    def delete_loan(self):
        # Delete a loan based on loan_id
        loan_id = self.loan_id.get().strip()
        loan = self.loan_manager.get_loan(loan_id)
        if not loan:
            messagebox.showerror("Error", "Loan ID not found!")
            return

        self.loan_manager.delete_loan(loan_id)
        messagebox.showinfo("Success", "Loan deleted successfully!")
        self.clear_entries()

    def generate_summary(self):
        # Generate a summary of a loan based on loan_id
        loan_id = self.loan_id.get().strip()
        loan = self.loan_manager.get_loan(loan_id)
        if not loan:
            messagebox.showerror("Error", "Loan ID not found!")
            return

        summary = f"""
        Loan ID: {loan.loan_id}
        Amount: {loan.amount}
        Interest Rate: {loan.interest_rate}
        Term: {loan.term} years
        Start Date: {loan.start_date.strftime('%Y-%m-%d')}
        End Date: {loan.end_date.strftime('%Y-%m-%d')}
        Monthly Payment: {loan.monthly_payment:.2f}
        """
        messagebox.showinfo("Loan Summary", summary)

    def export_to_excel(self):
        # Export loans to an Excel file
        try:
            df = pd.DataFrame([loan.__dict__ for loan in self.loan_manager.get_loans()])
            df.to_excel('loans.xlsx', index=False)
            messagebox.showinfo("Success", "Data exported to loans.xlsx!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No loans found!")
        except ModuleNotFoundError:
            messagebox.showerror("Error", "openpyxl library not found! Please install it using 'pip install openpyxl'.")

    def plot_insights(self):
        # Plot financial insights based on loan data
        loans = self.loan_manager.get_loans()
        if not loans:
            messagebox.showerror("Error", "No loans found to plot insights!")
            return

        df = pd.DataFrame([loan.__dict__ for loan in loans])
        plt.figure(figsize=(15, 10))

        plt.subplot(2, 2, 1)
        df.groupby("start_date")["amount"].sum().plot(kind="bar")
        plt.title("Total Loan Amount by Start Date")
        plt.xlabel("Start Date")
        plt.ylabel("Total Amount")

        plt.subplot(2, 2, 2)
        df["interest_rate"].plot(kind="hist", bins=10)
        plt.title("Interest Rate Distribution")
        plt.xlabel("Interest Rate")

        plt.subplot(2, 2, 3)
        df.groupby("start_date")["monthly_payment"].sum().plot(kind="line")
        plt.title("Monthly Payments Over Time")
        plt.xlabel("Start Date")
        plt.ylabel("Monthly Payment")

        plt.subplot(2, 2, 4)
        df["term"].value_counts().plot(kind="pie", autopct='%1.1f%%')
        plt.title("Loan Terms Distribution")

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = LoanApp()
    app.mainloop()
